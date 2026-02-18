"""
Claude Opus 4.6 - Streaming Responses
=======================================
Stream tokens as they arrive for real-time UX in data pipelines.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 02_streaming.py
"""

import os
from dotenv import load_dotenv
import anthropic

load_dotenv()


def stream_response(prompt: str, system: str = "") -> str:
    """Stream a Claude Opus 4.6 response token by token."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    collected = []
    with client.messages.stream(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            collected.append(text)

    print()
    return "".join(collected)


def stream_with_metadata(prompt: str, system: str = "") -> dict:
    """Stream response and capture usage metadata."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    collected_text = []
    input_tokens = 0
    output_tokens = 0

    with client.messages.stream(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for event in stream:
            if hasattr(event, "type"):
                if event.type == "content_block_delta":
                    collected_text.append(event.delta.text)
                    print(event.delta.text, end="", flush=True)
                elif event.type == "message_delta":
                    output_tokens = event.usage.output_tokens

        input_tokens = stream.get_final_message().usage.input_tokens

    print()
    return {
        "text": "".join(collected_text),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
    }


if __name__ == "__main__":
    system_prompt = "You are a data engineering expert. Be concise."
    user_prompt = (
        "Write a PySpark script that reads Parquet from S3, "
        "deduplicates on event_id, and writes to BigQuery."
    )

    print("=== Streaming Claude Opus 4.6 ===\n")
    result = stream_with_metadata(user_prompt, system=system_prompt)
    print(
        f"\n--- Usage: {result['input_tokens']} in / {result['output_tokens']} out ---"
    )
