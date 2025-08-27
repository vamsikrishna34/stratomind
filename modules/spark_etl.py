"""
spark_etl.py — Data ingestion and transformation with Spark (stub mode).

Switch `USE_SPARK=True` when deploying in a Spark-enabled environment.
"""

import os
import io
import pandas as pd

# Toggle for real Spark usage
USE_SPARK = False

try:
    if USE_SPARK:
        from pyspark.sql import SparkSession
except ImportError:
    pass  # Ignore if Spark isn't installed yet


def run_etl(input_source):
    """
    Runs ETL pipeline on the provided dataset.

    Args:
        input_source (str | file-like | pd.DataFrame):
            - Path to the input CSV
            - File-like object (e.g. from Streamlit uploader)
            - Pandas DataFrame (skips loading step)

    Returns:
        pd.DataFrame or pyspark.sql.DataFrame: Transformed data.
    """
    if USE_SPARK:
        spark = (
            SparkSession.builder
            .appName("StratoMind ETL")
            .config("spark.sql.shuffle.partitions", "8")
            .getOrCreate()
        )

        if isinstance(input_source, str):
            df = spark.read.csv(input_source, header=True, inferSchema=True)
        elif hasattr(input_source, "read"):  # file-like object
            # Spark can't read file-like directly — save temp then read
            tmp_path = "_temp_upload.csv"
            with open(tmp_path, "wb") as tmp_f:
                tmp_f.write(input_source.read())
            df = spark.read.csv(tmp_path, header=True, inferSchema=True)
            os.remove(tmp_path)
        else:
            raise ValueError("Unsupported input type for Spark ETL.")

        return _transform_spark(df)

    else:
        # Pandas fallback
        if isinstance(input_source, pd.DataFrame):
            df = input_source
        elif isinstance(input_source, str):
            if not os.path.exists(input_source):
                raise FileNotFoundError(f"No file found at {input_source}")
            df = pd.read_csv(input_source)
        elif hasattr(input_source, "read"):  # file-like
            df = pd.read_csv(input_source)
        else:
            raise ValueError("Unsupported input type for Pandas ETL.")

        return _transform_pandas(df)


def _transform_spark(df):
    """Example Spark transformations."""
    return (
        df.dropna()
          .withColumnRenamed("old_column", "new_column")
    )


def _transform_pandas(df):
    """Example Pandas transformations (stub)."""
    return (
        df.dropna()
          .rename(columns=lambda c: c.strip().lower().replace(" ", "_"))
    )