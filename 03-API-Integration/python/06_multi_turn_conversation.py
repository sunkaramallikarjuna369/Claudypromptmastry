"""
Claude Opus 4 - Multi-Turn Conversation for Data Engineering
==============================================================
Build conversational data engineering assistants with context memory.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 06_multi_turn_conversation.py
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

SYSTEM_PROMPT = """You are a data engineering assistant powered by Claude Opus 4.
You help users with:
- Writing SQL queries (BigQuery, PostgreSQL, Snowflake)
- Building ETL pipelines (Spark, Pandas, Dataflow)
- Infrastructure as code (Terraform, Pulumi)
- Data modeling and schema design
- Performance optimization

Maintain context across the conversation. Reference previous queries and build on them.
Be concise but thorough. Always include error handling in generated code."""


class DataEngineeringAssistant:
    """A multi-turn conversational assistant for data engineering tasks."""

    def __init__(self, model: str = "claude-opus-4-20250514"):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model
        self.messages: list[dict] = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def chat(self, user_message: str) -> str:
        """Send a message and get a response, maintaining conversation history."""
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=self.messages,
        )

        assistant_text = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_text})

        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return assistant_text

    def get_usage(self) -> dict:
        """Get cumulative token usage."""
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_turns": len(self.messages) // 2,
            "estimated_cost": round(
                (self.total_input_tokens * 0.015 + self.total_output_tokens * 0.075)
                / 1000,
                4,
            ),
        }

    def reset(self):
        """Reset conversation history."""
        self.messages = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0


if __name__ == "__main__":
    assistant = DataEngineeringAssistant()

    conversation = [
        "I have a BigQuery table `analytics.raw_events` with columns: "
        "event_id, user_id, event_type, timestamp, metadata (JSON). "
        "Help me design a star schema for this data.",
        "Now write the BigQuery DDL to create these tables with "
        "appropriate partitioning and clustering.",
        "Generate a dbt model that transforms raw_events into the fact table, "
        "including deduplication and JSON parsing.",
        "What data quality tests should I add for these models?",
    ]

    print("=== Claude Opus 4 Multi-Turn Assistant ===\n")

    for i, msg in enumerate(conversation, 1):
        print(f"[Turn {i}] User: {msg[:80]}...")
        response = assistant.chat(msg)
        print(f"[Turn {i}] Claude: {response[:300]}...\n")
        print("-" * 60)

    usage = assistant.get_usage()
    print(f"\nUsage: {usage}")
