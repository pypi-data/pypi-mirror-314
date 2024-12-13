import logging
import glob

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('monitoring.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class FileMonitor:
    def __init__(self, pattern: str):
        self.pattern = pattern

    def monitor_files(self):
        """Monitor files based on the provided glob pattern."""
        logger.info(f"Starting monitoring with pattern: {self.pattern}")
        try:
            matching_files = glob.glob(self.pattern)
            if matching_files:
                logger.info(f"Found {len(matching_files)} file(s) matching the pattern.")
                for file in matching_files:
                    logger.info(f"Monitoring file: {file}")
            else:
                logger.warning(f"No files found matching pattern: {self.pattern}")
        except Exception as e:
            logger.error(f"Error while monitoring files: {e}")

class ByteConverterMonitor:
    @staticmethod
    def log_conversion_info(byte_seq: bytes, result: str):
        """Log information about byte-to-int conversion."""
        logger.debug(f"Conversion for byte sequence {byte_seq.hex()}: {result}")
    
    @staticmethod
    def log_int_to_bytes(value: int, result: str):
        """Log information about int-to-byte conversion."""
        logger.debug(f"Conversion for value {value}: {result}")