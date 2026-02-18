"""
Claude Opus 4.6 - Basic API Client
===================================
Three ways to connect: Anthropic Direct, AWS Bedrock, Google Vertex AI.

Usage:
    pip install anthropic python-dotenv
    export ANTHROPIC_API_KEY=sk-ant-...
    python 01_basic_client.py
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


def anthropic_direct(prompt: str, system: str = "") -> str:
    """Call Claude Opus 4.6 via the Anthropic direct API."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def bedrock_client(prompt: str, system: str = "") -> str:
    """Call Claude Opus 4.6 via AWS Bedrock."""
    import boto3
    import json

    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        body["system"] = system

    response = bedrock.invoke_model(
        modelId="anthropic.claude-opus-4-20250514-v1:0",
        body=json.dumps(body),
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


def vertex_client(prompt: str, system: str = "", project_id: str = "") -> str:
    """Call Claude Opus 4.6 via Google Vertex AI."""
    from anthropic import AnthropicVertex

    client = AnthropicVertex(
        region="us-east5",
        project_id=project_id or os.environ.get("GCP_PROJECT_ID", ""),
    )

    message = client.messages.create(
        model="claude-opus-4@20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


if __name__ == "__main__":
    system_prompt = (
        "You are a senior data engineer specializing in GCP BigQuery and ETL pipelines."
    )
    user_prompt = (
        "Generate a BigQuery SQL query that calculates daily revenue "
        "by product category with a 7-day rolling average. "
        "Tables: analytics.orders (order_id, product_id, amount, order_date), "
        "analytics.products (product_id, category, name)."
    )

    print("--- Anthropic Direct API ---")
    result = anthropic_direct(user_prompt, system=system_prompt)
    print(result)
