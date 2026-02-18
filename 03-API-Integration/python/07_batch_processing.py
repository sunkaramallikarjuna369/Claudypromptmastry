"""
Claude Opus 4.6 - Batch Processing for Data Engineering
=========================================================
Process multiple prompts efficiently using the Anthropic Batch API.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 07_batch_processing.py
"""

import os
import time
from dotenv import load_dotenv
import anthropic

load_dotenv()

BATCH_TASKS = [
    {
        "id": "sql_optimization",
        "prompt": (
            "Optimize this BigQuery query for cost and performance:\n"
            "SELECT * FROM analytics.orders o "
            "JOIN analytics.products p ON o.product_id = p.product_id "
            "WHERE o.order_date > '2025-01-01'"
        ),
    },
    {
        "id": "schema_review",
        "prompt": (
            "Review this table schema and suggest improvements:\n"
            "CREATE TABLE events (id INT64, data STRING, ts TIMESTAMP, user STRING)"
        ),
    },
    {
        "id": "pipeline_code",
        "prompt": "Write a Python function that validates CSV data before loading to BigQuery.",
    },
    {
        "id": "terraform_module",
        "prompt": (
            "Generate a Terraform module for a BigQuery dataset with "
            "two tables, IAM bindings, and scheduled queries."
        ),
    },
    {
        "id": "error_handling",
        "prompt": (
            "Write a Python retry decorator with exponential backoff "
            "suitable for BigQuery API calls."
        ),
    },
]


def run_batch_sync(tasks: list[dict]) -> list[dict]:
    """Process multiple prompts sequentially (for smaller batches)."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    results = []

    for task in tasks:
        print(f"Processing: {task['id']}...")
        response = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": task["prompt"]}],
        )
        results.append(
            {
                "id": task["id"],
                "response": response.content[0].text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
            }
        )

    return results


def run_batch_api(tasks: list[dict]) -> str:
    """Submit tasks using the Anthropic Message Batches API for 50% cost savings."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    requests = []
    for task in tasks:
        requests.append(
            anthropic.types.batch_create_params.Request(
                custom_id=task["id"],
                params=anthropic.types.MessageCreateParamsNonStreaming(
                    model="claude-opus-4-20250514",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": task["prompt"]}],
                ),
            )
        )

    batch = client.messages.batches.create(requests=requests)
    print(f"Batch created: {batch.id}")
    print(f"Status: {batch.processing_status}")

    while batch.processing_status != "ended":
        time.sleep(10)
        batch = client.messages.batches.retrieve(batch.id)
        print(
            f"Status: {batch.processing_status} "
            f"({batch.request_counts.succeeded}/{batch.request_counts.processing})"
        )

    results = []
    for result in client.messages.batches.results(batch.id):
        results.append(
            {
                "id": result.custom_id,
                "type": result.result.type,
                "response": (
                    result.result.message.content[0].text
                    if result.result.type == "succeeded"
                    else str(result.result.error)
                ),
            }
        )

    return results


if __name__ == "__main__":
    print("=== Claude Opus 4.6 Batch Processing ===\n")
    print(f"Tasks to process: {len(BATCH_TASKS)}")
    for task in BATCH_TASKS:
        print(f"  - {task['id']}: {task['prompt'][:60]}...")

    print("\nProcessing sequentially...")
    results = run_batch_sync(BATCH_TASKS)

    for r in results:
        print(f"\n--- {r['id']} ({r['input_tokens']}+{r['output_tokens']} tokens) ---")
        print(r["response"][:200] + "...")
