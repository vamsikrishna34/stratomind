"""
spark_etl.py — Data ingestion and transformation with Spark or Pandas.

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
    pass


def run_etl(input_source):
    """
    Runs ETL pipeline on the provided dataset.

    Args:
        input_source (str | file-like | pd.DataFrame):
            - Path to the input CSV
            - File-like object (e.g., from Streamlit uploader)
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
        elif hasattr(input_source, "read"):  # file-like object
            df = pd.read_csv(input_source)
        else:
            raise ValueError("Unsupported input type for Pandas ETL.")

        return _transform_pandas(df)


# ----------------------
# Spark Transformation
# ----------------------
def _transform_spark(df):
    """Example Spark transformations."""
    return (
        df.dropna()
          .withColumnRenamed("old_column", "new_column")
    )


# ----------------------
# Pandas Transformation
# ----------------------
def _transform_pandas(df):
    """
    Pandas transformations:
    - Clean column names
    - If only a `content` column exists (from PDF/DOCX), derive title/description
    - Extract simple NLP features
    """
    # Clean column names
    df = df.rename(columns=lambda c: c.strip().lower().replace(" ", "_"))

    # Drop full-empty rows (but keep 0s)
    df = df.dropna(how="all")

    # Handle pure text extraction case
    if set(df.columns) == {"content"}:
        from textblob import TextBlob

        # Ensure strings
        df["content"] = df["content"].astype(str)

        # Derive a pseudo title and description
        df["title"] = df["content"].apply(lambda x: x.split("\n")[0][:80] if x else "")
        df["description"] = df["content"].apply(lambda x: " ".join(x.split()[1:50]) if len(x.split()) > 1 else "")

        # Basic keyword extraction & sentiment
        df["char_count"] = df["content"].apply(len)
        df["word_count"] = df["content"].apply(lambda x: len(x.split()))
        df["keywords"] = df["content"].apply(lambda x: ", ".join(sorted(set(x.split()[:5]))))
        df["sentiment_polarity"] = df["content"].apply(lambda x: round(TextBlob(x).sentiment.polarity, 3))

    else:
        # Convert all object columns to strings to avoid .lower() errors later
        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].astype(str)

    return df