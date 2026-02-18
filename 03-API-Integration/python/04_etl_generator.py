"""
Claude Opus 4.6 - ETL Pipeline Generator
==========================================
Use Claude to generate production-ready ETL pipelines with structured output.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 04_etl_generator.py
"""

import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

ETL_SYSTEM_PROMPT = """You are a senior data engineer. When asked to generate ETL pipelines, respond with valid JSON matching this schema:

{
  "pipeline_name": "string",
  "description": "string",
  "source": {
    "type": "s3|gcs|bigquery|postgres|api",
    "location": "string",
    "format": "parquet|csv|json|avro",
    "schema": [{"name": "string", "type": "string"}]
  },
  "transforms": [
    {
      "step": "integer",
      "operation": "string",
      "description": "string",
      "code": "string (Python/SQL)"
    }
  ],
  "sink": {
    "type": "bigquery|s3|gcs|postgres",
    "location": "string",
    "write_mode": "append|overwrite|merge",
    "partitioning": {"field": "string", "type": "DAY|MONTH|YEAR"},
    "clustering": ["string"]
  },
  "quality_checks": [
    {"check": "string", "threshold": "string"}
  ],
  "code": "string (complete runnable Python code)"
}"""


def generate_etl_pipeline(description: str) -> dict:
    """Generate a complete ETL pipeline spec from a natural language description."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=8192,
        system=ETL_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": description}],
    )

    response_text = message.content[0].text

    start = response_text.find("{")
    end = response_text.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(response_text[start:end])
    return {"raw_response": response_text}


def generate_pandas_cleaning_script(schema_description: str) -> str:
    """Generate a Pandas data cleaning script using Claude Opus 4.6."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""Generate a complete, runnable Python script using Pandas that:
1. Reads the data (provide a sample DataFrame creation for testing)
2. Identifies anomalies (nulls, outliers, format issues)
3. Cleans the data with:
   - Null handling (mean/median/mode per column type)
   - Outlier detection using IQR
   - Date format standardization
   - String normalization
4. Adds logging
5. Outputs a quality report

Schema: {schema_description}

Return ONLY the Python code, no explanations."""

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def generate_spark_pipeline(specs: str) -> str:
    """Generate a PySpark ETL pipeline from specifications."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = f"""Generate a complete PySpark ETL pipeline with:
- SparkSession creation
- Source reading with schema inference
- All specified transformations
- Data quality validation
- Sink writing with partitioning
- Error handling and logging
- Unit test examples

Specifications:
{specs}

Return ONLY the Python code."""

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


if __name__ == "__main__":
    pipeline_desc = (
        "Build an ETL pipeline that reads customer order data from S3 Parquet files, "
        "deduplicates on order_id, joins with a BigQuery product dimension table, "
        "calculates daily revenue aggregates, and writes results to BigQuery "
        "partitioned by order_date and clustered by product_category."
    )

    print("=== Claude Opus 4.6 ETL Generator ===\n")
    print(f"Generating pipeline for: {pipeline_desc[:80]}...\n")

    pipeline = generate_etl_pipeline(pipeline_desc)
    print(json.dumps(pipeline, indent=2))
