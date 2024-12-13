
from typing import Dict, Any, Optional, Union, List


async def process_column_data(column_data: List[str], scanner, sample_size: Optional[Union[int, float]], region) -> Dict[str, Any]:
    """
    Process column data using NER Scanner.
    """
    return await scanner.scan(column_data, sample_size=sample_size, region=region)