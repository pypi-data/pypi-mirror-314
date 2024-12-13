import json
import logging
from pii_scanner.ner.ner_scanner import SpacyNERScanner

from typing import Dict, Any, Optional, Union, List
from pii_scanner.utils.csv_file import read_csv, extract_column_data, clean_data
from pii_scanner.file_readers.process_column import process_column_data


# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# async def process_column_data(column_data: List[str], scanner, sample_size: Optional[Union[int, float]], region) -> Dict[str, Any]:
#     """
#     Process column data using NER Scanner.
#     """
#     return await scanner.scan(column_data, sample_size=sample_size, region=region)

async def csv_file_pii_detector(file_path: str,  sample_size: Optional[Union[int, float]] = None, region=None) -> Dict[str, Any]:
    """
    """
    scanner = SpacyNERScanner()  # Initialize your NER Scanner
    
    try:
        # Read CSV file
        data = read_csv(file_path)
        logger.info(f"Successfully read file: {file_path}")

        # Check if data is empty
        if not data:
            logger.warning("No data found in the file.")
            return {"error": "No data found in the file."}

        # Initialize a dictionary to store results
        results = {}

        column_name = None
        # Process the specified column or all columns if not specified
        columns_to_process = [column_name] if column_name and column_name in data[0] else list(data[0].keys())

        # Process each column sequentially
        for col in columns_to_process:
            logger.info(f"Processing column: {col}")
            try:
                column_data = clean_data(extract_column_data(data, col))
                result = await process_column_data(column_data, scanner, sample_size, region=region)
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

