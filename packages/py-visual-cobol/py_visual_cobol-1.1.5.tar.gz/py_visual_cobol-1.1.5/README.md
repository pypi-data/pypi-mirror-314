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
from pyspark.sql.types import StructType, StructField, IntegerType, BinaryType
from py_visual_cobol.record_extractor import record_header_extractor
from pyspark.sql import SparkSession,functions as F
from pyspark import StorageLevel
import argparse
import mmap


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Process a microfile.")
    parser.add_argument("file_path", type=str, help="Path to the microfile.")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Read the file content
    with open(args.file_path, mode="rb") as file:
        # Use mmap to map the file into memory
        with mmap.mmap(file.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
            # Read data in a memory-efficient way
            content = mmapped_file[:]  # Only extract bytes as needed

    records_length = [
            126,
            836,
            96,
            694,
            302,
        ]

    # Extract records using the segment patterns generated
    records = record_header_extractor(content,records_length=records_length,debug=True)
    
    print(len(records))
    spark = SparkSession.builder \
        .appName('app') \
        .config("spark.executor.memory", "8g") \
        .config("spark.driver.memory", "8g") \
        .config("spark.executor.cores", "8") \
        .config("spark.driver.maxResultSize", "0") \
        .config("spark.dynamicAllocation.enabled", "true") \
        .getOrCreate()


    # Define schema for the DataFrame


    schema = StructType([
        StructField("rdw", IntegerType(), True),
        StructField("value", BinaryType(), True)
    ])

    df = spark.createDataFrame(records, schema=schema)

    records.clear()

    df.persist(StorageLevel.DISK_ONLY)

    df.write.partitionBy("rdw").mode("overwrite").parquet("data", compression="snappy")
    df.unpersist(True)
    spark.stop()
```