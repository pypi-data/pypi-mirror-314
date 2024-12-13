import csv
from typing import List, Dict, Any

def read_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Read a CSV file and return its content as a list of dictionaries.
    """
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def extract_column_data(data: List[Dict[str, str]], column_name: str) -> List[str]:
    """
    Extract data from a specific column.
    """
    return [row.get(column_name, '') for row in data]

def clean_data(data: List[str]) -> List[str]:
    """
    Clean the data by removing leading/trailing spaces and filtering out empty strings.
    """
    return [text.strip() for text in data if text.strip()]



