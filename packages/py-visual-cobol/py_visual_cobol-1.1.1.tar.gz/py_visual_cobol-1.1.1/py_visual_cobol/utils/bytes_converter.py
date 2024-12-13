from typing import Optional

from py_visual_cobol.constants.params import (
    NORMAL_USER_DATA_RECORD_PREFIX,
    MAX_RECORD_LENGTH,
    FILE_HEADER_LENGTH,
    SYSTEM_RECORD_PREFIX
)

from py_visual_cobol.helper.monitoring import ByteConverterMonitor

class ByteConverter:
    @staticmethod
    def bytes_to_int(byte_seq: bytes) -> Optional[int]:
        try:
            if len(byte_seq) < 2:
                ByteConverterMonitor.log_conversion_info(byte_seq, "Byte sequence too short")
                return None
            
            result = int.from_bytes(byte_seq, byteorder='big') & MAX_RECORD_LENGTH
            return result
        
        except Exception as e:
            ByteConverterMonitor.log_conversion_info(byte_seq, f"error:{e}")
            return None


    @staticmethod
    def int_to_bytes(value: int) -> Optional[bytes]:
        try:
            if value < 0 or value > MAX_RECORD_LENGTH:
                ByteConverterMonitor.log_int_to_bytes(value, "Value out of range")
                return None
            
            if value == FILE_HEADER_LENGTH:
                binary_str = f"{SYSTEM_RECORD_PREFIX}{value:012b}"
                result = int(binary_str, 2).to_bytes(2, byteorder='big')
                return result
            
            binary_str = f"{NORMAL_USER_DATA_RECORD_PREFIX}{value:012b}"
            result = int(binary_str, 2).to_bytes(2, byteorder='big')
            return result
        
        except Exception as e:
            ByteConverterMonitor.log_int_to_bytes(value, f"Error: {e}")
            return None
