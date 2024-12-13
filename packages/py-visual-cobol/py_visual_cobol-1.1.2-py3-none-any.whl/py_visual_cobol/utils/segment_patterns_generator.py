from typing import Dict, Tuple
from py_visual_cobol.utils.bytes_converter import ByteConverter


def generate_segment_patterns(segment_lengths: list) -> Dict[int, Tuple[bytes, str]]:
    """
    Generates a dictionary of segment patterns.

    Args:
        segment_lengths (list): List of segment lengths to convert.

    Returns:
        dict: A dictionary mapping each segment length to its byte representation and hex value.
    """
    
    return {
        length: (byte_value, byte_value.hex())
        for length in segment_lengths
        if (byte_value := ByteConverter.int_to_bytes(length)) is not None
    }
