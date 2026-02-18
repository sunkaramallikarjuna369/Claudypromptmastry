"""
Claude Opus 4.6 - Tool Calling (Function Calling)
===================================================
Define tools Claude can invoke to interact with databases, APIs, and files.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 03_tool_calling.py
"""

import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()

TOOLS = [
    {
        "name": "execute_sql",
        "description": "Execute a SQL query against BigQuery and return results as JSON.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The BigQuery SQL query to execute.",
                },
                "project_id": {
                    "type": "string",
                    "description": "GCP project ID.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a data file (CSV, JSON, Parquet) and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the data file.",
                },
                "format": {
                    "type": "string",
                    "enum": ["csv", "json", "parquet"],
                    "description": "File format.",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max rows to return.",
                    "default": 100,
                },
            },
            "required": ["file_path", "format"],
        },
    },
    {
        "name": "run_data_quality_check",
        "description": "Run data quality checks on a dataset: null counts, duplicates, schema validation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Fully qualified table name (project.dataset.table).",
                },
                "checks": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "nulls",
                            "duplicates",
                            "schema",
                            "freshness",
                            "row_count",
                        ],
                    },
                    "description": "List of quality checks to run.",
                },
            },
            "required": ["table_name", "checks"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file on disk.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Output file path.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
]


def handle_tool_call(tool_name: str, tool_input: dict) -> str:
    """Simulate tool execution. Replace with real implementations."""
    if tool_name == "execute_sql":
        return json.dumps(
            {
                "status": "success",
                "rows_returned": 42,
                "sample_data": [
                    {
                        "category": "Electronics",
                        "daily_total": 15230.50,
                        "rolling_avg": 14890.20,
                    },
                    {
                        "category": "Books",
                        "daily_total": 3420.00,
                        "rolling_avg": 3150.75,
                    },
                ],
            }
        )
    elif tool_name == "read_file":
        return json.dumps(
            {
                "status": "success",
                "rows": 1000,
                "columns": ["id", "name", "amount", "date"],
                "sample": [
                    {"id": 1, "name": "Alice", "amount": 99.99, "date": "2026-01-15"},
                ],
            }
        )
    elif tool_name == "run_data_quality_check":
        return json.dumps(
            {
                "status": "success",
                "results": {
                    "nulls": {"email": 52, "phone": 210},
                    "duplicates": {"count": 3, "on_column": "id"},
                    "row_count": 50000,
                },
            }
        )
    elif tool_name == "write_file":
        return json.dumps(
            {"status": "success", "path": tool_input.get("file_path", "")}
        )
    return json.dumps({"status": "error", "message": f"Unknown tool: {tool_name}"})


def run_with_tools(prompt: str, system: str = "") -> str:
    """Run a multi-turn conversation where Claude can call tools."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    messages = [{"role": "user", "content": prompt}]

    while True:
        response = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=4096,
            system=system,
            tools=TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            return final_text

        tool_results = []
        assistant_content = []
        for block in response.content:
            if block.type == "text":
                assistant_content.append(block)
                print(f"[Claude]: {block.text}")
            elif block.type == "tool_use":
                assistant_content.append(block)
                print(f"[Tool Call]: {block.name}({json.dumps(block.input, indent=2)})")
                result = handle_tool_call(block.name, block.input)
                print(f"[Tool Result]: {result[:200]}...")
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    system_prompt = (
        "You are a data engineering agent with access to BigQuery, file I/O, "
        "and data quality tools. Use the tools to complete the user's request."
    )
    user_prompt = (
        "Check the data quality of the table myproject.analytics.orders. "
        "Run null checks and duplicate checks, then write a summary report."
    )

    print("=== Claude Opus 4.6 Tool Calling ===\n")
    final = run_with_tools(user_prompt, system=system_prompt)
    print(f"\n--- Final Response ---\n{final}")
