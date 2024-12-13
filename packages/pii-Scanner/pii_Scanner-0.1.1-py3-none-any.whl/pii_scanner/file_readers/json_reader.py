import json
import logging
from typing import Dict, Any, Optional, Union, List
from pii_scanner.ner.ner_scanner import SpacyNERScanner

from pii_scanner.utils.json_file import read_json, extract_column_data, clean_data
from pii_scanner.file_readers.process_column import process_column_data


# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def json_file_pii_detector(file_path: str, sample_size: Optional[Union[int, float]] = None, region=None) -> Dict[str, Any]:
    """
    Main function to detect PII in a JSON file.
    """
    scanner = SpacyNERScanner()   # Initialize your NER Scanner

    try:
        # Read JSON file
        data = read_json(file_path)
        logger.info(f"Successfully read file: {file_path}")

        # Check if data is empty
        if not data:
            logger.warning("No data found in the file.")
            return {"error": "No data found in the file."}

        # Initialize a dictionary to store results
        results = {}

        # Process the specified column or all columns if not specified
        column_name = None
        columns_to_process = [column_name] if column_name and column_name in data[0] else list(data[0].keys())
        print(columns_to_process)
        # Process each column sequentially
        for col in columns_to_process:
            logger.info(f"Processing column: {col}")
            try:
                column_data = clean_data(extract_column_data(data, col))
                result = await process_column_data(column_data, scanner, sample_size, region=region)
                print(result)
                results[col] = result
            except Exception as e:
                logger.error(f"Error processing column: {col} - {e}")
                results[col] = {"error": str(e)}

        logger.info("Processing completed successfully.")
        return results

    except FileNotFoundError:
        error_message = f"Error: The file '{file_path}' was not found."
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {"error": str(e)}

