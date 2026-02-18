"""
Claude Opus 4 - Agentic Data Engineering Workflow
===================================================
Multi-step agent that plans, executes, validates, and reports on data tasks.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 05_agentic_workflow.py
"""

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

AGENT_SYSTEM = """You are a Data Engineering Agent powered by Claude Opus 4.
You operate in a PLAN-EXECUTE-VALIDATE-REPORT cycle.

Available tools:
1. execute_sql - Run BigQuery SQL queries
2. run_python - Execute Python/Pandas code
3. read_file - Read data files
4. write_file - Write output files
5. check_quality - Run data quality checks
6. send_alert - Send alerts on failures

For each task:
- First create a detailed execution plan
- Execute each step using the appropriate tool
- Validate results after each step
- Generate a final report with metrics

Always think step-by-step and explain your reasoning."""

AGENT_TOOLS = [
    {
        "name": "execute_sql",
        "description": "Run a BigQuery SQL query.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "SQL query to execute."},
                "dry_run": {
                    "type": "boolean",
                    "description": "If true, estimate cost without running.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "run_python",
        "description": "Execute Python code in a sandboxed environment.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code to execute."},
                "timeout_seconds": {
                    "type": "integer",
                    "description": "Execution timeout.",
                },
            },
            "required": ["code"],
        },
    },
    {
        "name": "check_quality",
        "description": "Run data quality checks on a BigQuery table.",
        "input_schema": {
            "type": "object",
            "properties": {
                "table": {
                    "type": "string",
                    "description": "Table name (project.dataset.table).",
                },
                "checks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Quality checks to run.",
                },
            },
            "required": ["table", "checks"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path."},
                "content": {"type": "string", "description": "File content."},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "send_alert",
        "description": "Send an alert notification.",
        "input_schema": {
            "type": "object",
            "properties": {
                "severity": {"type": "string", "enum": ["info", "warning", "critical"]},
                "message": {"type": "string", "description": "Alert message."},
                "channel": {"type": "string", "enum": ["slack", "email", "pagerduty"]},
            },
            "required": ["severity", "message"],
        },
    },
]


def simulate_tool(name: str, inputs: dict) -> str:
    """Simulate tool execution for demo purposes."""
    simulations = {
        "execute_sql": {
            "status": "success",
            "rows_affected": 15234,
            "bytes_processed": "2.3 GB",
            "execution_time_ms": 4520,
            "sample_rows": [
                {"date": "2026-02-17", "total_orders": 1523, "revenue": 45230.50},
                {"date": "2026-02-16", "total_orders": 1489, "revenue": 42100.25},
            ],
        },
        "run_python": {
            "status": "success",
            "output": "DataFrame processed: 50000 rows, 12 columns\nNull values cleaned: 234\nOutliers removed: 18",
            "execution_time_ms": 3200,
        },
        "check_quality": {
            "status": "success",
            "results": {
                "null_percentage": {"email": 1.2, "phone": 4.5, "address": 0.0},
                "duplicate_count": 3,
                "freshness_hours": 2.5,
                "row_count": 50000,
                "schema_valid": True,
            },
        },
        "write_file": {
            "status": "success",
            "path": inputs.get("path", "output.txt"),
            "bytes_written": 2048,
        },
        "send_alert": {
            "status": "sent",
            "channel": inputs.get("channel", "slack"),
            "timestamp": datetime.now().isoformat(),
        },
    }
    return json.dumps(simulations.get(name, {"status": "unknown_tool"}))


def run_agent(task: str, max_iterations: int = 10) -> str:
    """Run the agentic workflow with tool calling loop."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    messages = [{"role": "user", "content": task}]
    iteration = 0

    print(f"[Agent] Task: {task}\n")
    print("=" * 60)

    while iteration < max_iterations:
        iteration += 1
        print(f"\n[Iteration {iteration}]")

        response = client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=4096,
            system=AGENT_SYSTEM,
            tools=AGENT_TOOLS,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            print(f"\n[Agent Complete]\n{final_text}")
            return final_text

        tool_results = []
        assistant_content = []

        for block in response.content:
            if block.type == "text":
                assistant_content.append(block)
                print(f"  [Thinking]: {block.text[:200]}...")
            elif block.type == "tool_use":
                assistant_content.append(block)
                print(f"  [Tool]: {block.name}")
                print(f"  [Input]: {json.dumps(block.input, indent=2)[:300]}")

                result = simulate_tool(block.name, block.input)
                print(f"  [Result]: {result[:200]}")

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    }
                )

        messages.append({"role": "assistant", "content": assistant_content})
        messages.append({"role": "user", "content": tool_results})

    return "Agent reached maximum iterations."


if __name__ == "__main__":
    task = (
        "I need you to:\n"
        "1. Query BigQuery for yesterday's order data from analytics.orders\n"
        "2. Run data quality checks on the results (nulls, duplicates, freshness)\n"
        "3. If quality passes, write a summary report\n"
        "4. If any issues found, send a Slack alert"
    )

    print("=== Claude Opus 4 Agentic Workflow ===\n")
    run_agent(task)
