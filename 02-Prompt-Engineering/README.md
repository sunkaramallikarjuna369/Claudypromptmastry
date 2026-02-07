# Module 02: Prompt Engineering for Data Engineering

> **What** prompt techniques work best for data engineering tasks?
> **Who** can benefit from structured prompting approaches?
> **When** should you use each technique?
> **Where** do these techniques apply in the data pipeline lifecycle?
> **How** do you implement each technique effectively?

---

## Overview

This module teaches four advanced prompt engineering techniques specifically optimized for data engineering workflows with Claude Opus 4.6.

### 1. Explicit Specification (JSON Schemas)
Define exact output formats using JSON schemas so Claude generates precisely structured code and configurations.

```json
{
  "pipeline": {
    "name": "string",
    "source": { "type": "s3|gcs|bigquery", "path": "string" },
    "transforms": [{ "operation": "string", "params": {} }],
    "sink": { "type": "bigquery|s3", "config": {} },
    "quality_checks": [{ "rule": "string", "threshold": "number" }]
  }
}
```

### 2. Adaptive Chain-of-Thought (Plan > Execute > Validate)
Structure prompts to force Claude through a systematic reasoning process:

**Step 1 - PLAN:** Analyze the requirements and create an execution plan
**Step 2 - EXECUTE:** Generate the code/configuration following the plan
**Step 3 - VALIDATE:** Self-check the output against requirements

### 3. Parallel Tool Calling (BigQuery + API)
Leverage Claude's ability to call multiple tools simultaneously:
- Execute BigQuery queries while calling REST APIs
- Run data quality checks in parallel with transformations
- Fetch metadata from multiple sources simultaneously

### 4. Metacognitive Self-Review
Prompt Claude to review its own output:
```
After generating the code, review it for:
1. Correctness: Does it handle all edge cases?
2. Performance: Are there optimization opportunities?
3. Security: Are credentials handled safely?
4. Maintainability: Is the code well-structured?
```

---

## Prompt Templates

### Template 1: ETL with Explicit Spec
```
You are a senior data engineer. Generate a {framework} ETL pipeline.

OUTPUT FORMAT (strict JSON):
{schema}

REQUIREMENTS:
- Source: {source_description}
- Transforms: {transform_list}
- Sink: {sink_description}
- Include error handling and logging
```

### Template 2: CoT Data Pipeline
```
TASK: Build a data pipeline for {use_case}

STEP 1 - PLAN:
- List all data sources and their schemas
- Define the transformation logic
- Specify output format and destination

STEP 2 - EXECUTE:
- Write the complete pipeline code
- Include all imports and configurations
- Add error handling

STEP 3 - VALIDATE:
- Check code for syntax errors
- Verify all requirements are met
- List any assumptions made
```

### Template 3: Parallel Tool Calling
```
Execute these tasks in parallel:
1. Query BigQuery: SELECT COUNT(*) FROM dataset.table WHERE date = CURRENT_DATE()
2. Fetch API: GET https://api.example.com/pipeline/status
3. Check S3: List files in s3://bucket/path/

Combine results into a pipeline status report.
```

### Template 4: Metacognitive Review
```
Generate a {task_description}.

After generating, perform a self-review:
- Score each dimension 1-10 (correctness, completeness, efficiency, security)
- List top 3 improvements
- Provide the improved version if any score < 8
```

---

## Quiz

Complete the 10-question quiz in the interactive dashboard.

**Open the interactive module:** [index.html](./index.html)

---

*Next: [Module 03 - API Integration](../03-API-Integration/)*
