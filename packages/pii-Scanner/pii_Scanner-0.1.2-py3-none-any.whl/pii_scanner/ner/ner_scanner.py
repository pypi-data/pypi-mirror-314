import time
import logging
import random
import asyncio
from typing import Dict, List, Union
from pii_scanner.regex_patterns.all_patterns import patterns
from presidio_analyzer.nlp_engine.spacy_nlp_engine import SpacyNlpEngine

logger = logging.getLogger(__name__)

class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_spacy_model):
        super().__init__()
        self.nlp = {"en": loaded_spacy_model}
                    
class SpacyNERScanner:
    """
    NER Scanner using Presidio's AnalyzerEngine with SpaCy 
    """

    SPACY_EN_MODEL = "en_core_web_lg"

    def __init__(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize variables for lazy loading
        self.analyzer = None
        self.nlp_engine = None
        self.initialized = False
        self.region = None

    def _initialize(self):
        """Lazy initialization of the SpaCy model and Presidio Analyzer."""
        if not self.initialized:
            import spacy
            from presidio_analyzer import AnalyzerEngine, PatternRecognizer

            try:
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)
            except OSError:
                self.logger.warning(
                    "Downloading en_core_web_md language model for SpaCy"
                )
                from spacy.cli import download
                download(self.SPACY_EN_MODEL)
                self.nlp_engine = spacy.load(self.SPACY_EN_MODEL)

            # Pass the loaded model to the new LoadedSpacyNlpEngine
            loaded_nlp_engine = LoadedSpacyNlpEngine(loaded_spacy_model=self.nlp_engine)

            # Pass the engine to the analyzer
            self.analyzer = AnalyzerEngine(nlp_engine=loaded_nlp_engine)

            # Create recognizers with the defined patterns and add them in a single loop
            global_patterns = patterns.get("GLOBAL", {})
            region_patterns = patterns.get(self.region.value, {})

            # Combine pattern dictionaries
            combined_patterns = {**global_patterns, **region_patterns}

            recognizers = [
                PatternRecognizer(supported_entity=entity, patterns=[pattern])
                for entity, pattern in combined_patterns.items()
            ]
            for recognizer in recognizers:
                self.analyzer.registry.add_recognizer(recognizer)

            self.initialized = True

    async def _process_with_analyzer_async(self, text: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        """
        Process a single text asynchronously using the Presidio Analyzer.
        """
        self._initialize()

        text = text.strip()
        try:
            analyzer_results = self.analyzer.analyze(text, language="en")
            result = {
                "text": text,
                "entity_detected": [{
                    "type": entity.entity_type,
                    "start": entity.start,
                    "end": entity.end,
                    "score": entity.score  # You can include the score if needed
                } for entity in analyzer_results]
            }
            return result
        except Exception as exc:
            self.logger.error(f"Error processing text '{text}': {exc}")
            return {
                "text": text,
                "entity_detected": []
            }

    async def _process_batch_async(self, texts: List[str]) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
        """
        Process a batch of texts concurrently using asyncio tasks.
        """
        tasks = [self._process_with_analyzer_async(text) for text in texts]
        return await asyncio.gather(*tasks)

    def _sample_data(self, sample_data: List[str], sample_size: Union[int, float]) -> List[str]:
        """
        Sample the data based on the sample_size, which can be an integer or a percentage.
        """
        total_data_length = len(sample_data)
        if isinstance(sample_size, float) and 0 < sample_size <= 1:
            sample_size = int(total_data_length * sample_size)
        elif isinstance(sample_size, int) and sample_size < total_data_length:
            sample_size = min(sample_size, total_data_length)
        else:
            sample_size = total_data_length

        return random.sample(sample_data, sample_size)
    
    async def scan(self, sample_data: List[str], sample_size, region: str) -> Dict[str, List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
        """
        Asynchronous version of the scan method.
        """
        start_time = time.time()
        self.region = region
        
        if sample_size:
            sample_data = self._sample_data(sample_data, sample_size)

        # Process the texts in parallel
        results = await self._process_batch_async(sample_data)

        end_time = time.time()
        processing_time = end_time - start_time
        self.logger.info(f"Processing completed in {processing_time:.2f} seconds.")

        return {
            "results": results
        }

    