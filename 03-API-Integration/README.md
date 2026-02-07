# Module 03: API Integration

> **What** APIs can you use to access Claude for data engineering?
> **Who** provides Claude API access (Anthropic, AWS, Google)?
> **When** should you use each provider?
> **Where** do API calls fit in your data pipeline?
> **How** do you set up and use each API effectively?

---

## Overview

This module covers three ways to access Claude Opus 4.6 for data engineering tasks, plus hands-on integration with GCP BigQuery and Python.

### Provider Comparison

| Feature | Anthropic Direct | AWS Bedrock | Google Vertex AI |
|---------|-----------------|-------------|-----------------|
| Setup Complexity | Low | Medium | Medium |
| GCP Integration | Manual | Via AWS | Native |
| Pricing | Pay-per-token | AWS pricing | GCP pricing |
| Max Context | 1M tokens | 1M tokens | 1M tokens |
| Tool Calling | Full support | Full support | Full support |
| Best For | Quick start | AWS shops | GCP shops |

### 1. Anthropic Direct API

```python
import anthropic

client = anthropic.Anthropic(api_key="sk-ant-...")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    system="You are a senior data engineer specializing in GCP.",
    messages=[{"role": "user", "content": "Generate a BigQuery SQL query..."}]
)
```

### 2. AWS Bedrock

```python
import boto3, json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
response = bedrock.invoke_model(
    modelId='anthropic.claude-sonnet-4-20250514-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": "..."}]
    })
)
```

### 3. Google Vertex AI

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(region="us-east5", project_id="my-project")
message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}]
)
```

---

## GCP BigQuery Integration Examples

### Example 1: Schema Analysis
```python
PROMPT = """
Analyze this BigQuery table schema and suggest:
1. Optimal partitioning strategy
2. Clustering columns
3. Data quality checks
4. Cost optimization tips

Schema:
{schema_json}
"""
```

### Example 2: Query Generation
```python
PROMPT = """
Write a BigQuery SQL query that:
- Calculates daily revenue by product category
- Includes 7-day rolling average
- Handles null values
- Optimizes for cost (partition pruning)

Tables available:
- analytics.orders (order_id, product_id, amount, order_date)
- analytics.products (product_id, category, name)
"""
```

### Example 3: Pandas + BigQuery Pipeline
```python
PROMPT = """
Generate Python code that:
1. Reads data from BigQuery using pandas-gbq
2. Cleans the data (handle nulls, outliers, types)
3. Performs aggregations
4. Writes results back to BigQuery

Use the google-cloud-bigquery library.
Include error handling and logging.
"""
```

---

## Quiz

Complete the 10-question quiz in the interactive dashboard.

**Open the interactive module:** [index.html](./index.html)

---

*Next: [Module 04 - Agentic Workflows](../04-Agentic-Workflows/)*
