```bash
py-visual-cobol
│
├───py_visual_cobol
│   ├───record_extractor.py
│   ├───__init__.py
│   │
│   ├───constants
│   │   ├───params.py
│   │   └───__init__.py
│   │
│   └───utils
│       ├───bytes_converter.py
│       ├───segment_patterns_generator.py
│       └─── __init__.py
├───tests
│   │   test_bytes_converter.py
│   │   test_segment_patterns_generator.py
│   └───__init__.py
│
├───poetry.lock
├───pyproject.toml
└───README.md
```


```python
import argparse
from py_visual_cobol.record_extractor import record_header_extractor


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process a microfile.")
    parser.add_argument("file_path", type=str, help="Path to the microfile.")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    with open("data/file.bin",mode='rb') as file:
        content = file.read()
    # Read the file content

    records_length = [
        126,
        836,
        96,
        694,
        302,
        160,
        107,
        76,
        266,
        68,
        99,
        78,
        425,
    ]

    # Extract records using the segment patterns generated
    records = record_header_extractor(content,records_length=records_length)

    # Print the extracted records
    print(records[0])
```