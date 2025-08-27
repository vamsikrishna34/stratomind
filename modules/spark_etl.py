"""
spark_etl.py — Data ingestion and transformation with Spark (stub mode).

Switch `USE_SPARK=True` when deploying in a Spark-enabled environment.
"""

import os
import pandas as pd

# Toggle for real Spark usage
USE_SPARK = False

try:
    if USE_SPARK:
        from pyspark.sql import SparkSession
except ImportError:
    pass  # Ignore if Spark isn't installed yet

def run_etl(input_path: str):
    """
    Runs ETL pipeline on the provided dataset.

    Args:
        input_path (str): Path to the input CSV or data source.

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
        df = spark.read.csv(input_path, header=True, inferSchema=True)
        df_cleaned = _transform_spark(df)
        return df_cleaned
    else:
        # Fallback to Pandas
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"No file found at {input_path}")
        df = pd.read_csv(input_path)
        df_cleaned = _transform_pandas(df)
        return df_cleaned

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