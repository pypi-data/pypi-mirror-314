from py_visual_cobol.utils.segment_patterns_generator import generate_segment_patterns
from py_visual_cobol.helper.monitoring import ByteConverterMonitor
from py_visual_cobol.utils.bytes_converter import ByteConverter
from typing import List, Dict


def record_header_extractor(content: bytes,records_length: list, debug: bool = False) -> List[Dict[str, bytes]]:
    """
    Extracts parts of a record from the given content using record lengths (rdw) and get corresponding record data.

    Args:
    content (bytes): The data to search through.
    records_length (list): A list of segment lengths (rdw values) to match in the data.
    debug (bool): monitoring the application using log file.

    Returns:
    List[Dict[str, bytes]]: A list of dictionaries, each containing the length and the corresponding record data.

    Example:
    >>> content = b'0~content1... CDcontent2...'
    >>> seg_patterns = [126, 836]
    >>> record_header_extractor(content, seg_patterns)
    [{'length': 126, 'record': b'content1'}, {'length': 836, 'record': b'content2'}]
    """
    records = []
    i = 0
    SEGMENT_PATTERNS = generate_segment_patterns(records_length)
    while i < len(content) - 1:
        try:
            segment = content[i:i+2]
            rdw = ByteConverter.bytes_to_int(segment)            
            if rdw in SEGMENT_PATTERNS:
                expected_segment, expected_hex = SEGMENT_PATTERNS[rdw]
                if segment == expected_segment and segment.hex() == expected_hex:
                    # check if the record start with 011 plus two space or not (this condition was fix 
                    # by skiping ahead the record len from rdw header)
                    # since the rdw header skip the bytes no need to use regex to handle other bytes 
                    # but just for make sure everything done perfectly instead of run with an issue.
                    data_slice = content[i + 2: i + 2 + rdw]
                    records.append({'rdw': rdw, 'value': data_slice})
                    i += 2 + rdw
                else:
                    i += 1
            else:
                i += 1
        except Exception as e:
            if debug:
                ByteConverterMonitor.log_conversion_info(segment, f"Error: {e} at Position: {i}")
    return records
