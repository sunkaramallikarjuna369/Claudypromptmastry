"""
Claude Opus 4 - Vision for Data Engineering
=============================================
Use Claude's vision capabilities to analyze charts, diagrams, and screenshots
of data pipeline dashboards.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python 08_vision_data_analysis.py
"""

import os
import base64
from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()


def analyze_image_from_file(image_path: str, prompt: str) -> str:
    """Analyze a local image file (chart, diagram, dashboard screenshot)."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    path = Path(image_path)
    media_type_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(path.suffix.lower(), "image/png")
    image_data = base64.standard_b64encode(path.read_bytes()).decode("utf-8")

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return message.content[0].text


def analyze_image_from_url(image_url: str, prompt: str) -> str:
    """Analyze an image from a URL."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "url", "url": image_url},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    return message.content[0].text


def analyze_erd_diagram(image_path: str) -> str:
    """Analyze an ERD diagram and generate DDL."""
    prompt = """Analyze this Entity-Relationship Diagram and:
1. List all entities and their attributes
2. Identify primary keys and foreign keys
3. Describe the relationships (1:1, 1:N, M:N)
4. Generate BigQuery DDL statements for all tables
5. Suggest partitioning and clustering strategies
6. Identify any normalization issues"""

    return analyze_image_from_file(image_path, prompt)


def analyze_pipeline_dashboard(image_path: str) -> str:
    """Analyze a data pipeline monitoring dashboard screenshot."""
    prompt = """Analyze this data pipeline monitoring dashboard and:
1. Identify any failed or degraded pipeline stages
2. Report on data freshness and latency metrics
3. Flag any anomalies in throughput or error rates
4. Suggest remediation steps for any issues
5. Rate overall pipeline health (healthy/degraded/critical)"""

    return analyze_image_from_file(image_path, prompt)


if __name__ == "__main__":
    print("=== Claude Opus 4 Vision for Data Engineering ===\n")
    print("Available functions:")
    print("  analyze_image_from_file(path, prompt) - Analyze local images")
    print("  analyze_image_from_url(url, prompt)   - Analyze images from URL")
    print("  analyze_erd_diagram(path)             - Parse ERD to DDL")
    print("  analyze_pipeline_dashboard(path)      - Monitor pipeline health")
    print("\nExample:")
    print('  result = analyze_erd_diagram("my_schema.png")')
    print('  result = analyze_pipeline_dashboard("grafana_screenshot.png")')
