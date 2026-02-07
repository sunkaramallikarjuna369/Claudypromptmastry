# Module 04: Agentic Workflows

> **What** are agentic workflows and how do they apply to data engineering?
> **Who** benefits from autonomous data pipeline agents?
> **When** should you use agentic vs single-shot prompting?
> **Where** do agents fit in the modern data stack?
> **How** do you build reliable agentic data engineering workflows?

---

## Overview

Agentic workflows allow Claude to autonomously plan, execute, and validate multi-step data engineering tasks. This module teaches you to build production-grade pipeline agents.

### The PLAN > EXECUTE > VALIDATE Loop

```
┌─────────┐     ┌─────────┐     ┌──────────┐
│  PLAN   │────>│ EXECUTE │────>│ VALIDATE │
│         │     │         │     │          │
│ Analyze │     │ Run SQL │     │ Check    │
│ Design  │     │ Run Code│     │ Quality  │
│ Estimate│     │ Call API│     │ Report   │
└─────────┘     └─────────┘     └──────────┘
      ^                              │
      └──────── ITERATE ─────────────┘
```

### Agent Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `execute_sql` | Run BigQuery queries | Schema analysis, data validation |
| `run_python` | Execute Python/Pandas | Data transformation, cleaning |
| `read_file` | Read data files | CSV, JSON, Parquet inspection |
| `write_file` | Write outputs | Reports, cleaned data, configs |
| `check_quality` | Run quality checks | Row counts, null rates, distributions |

### Building a Pipeline Agent

```python
SYSTEM_PROMPT = """
You are a Data Engineering Agent with access to these tools:
1. execute_sql(query) - Run BigQuery SQL
2. run_python(code) - Execute Python code
3. read_file(path) - Read files
4. write_file(path, content) - Write files
5. check_quality(dataset) - Quality checks

For every task, follow this workflow:
PLAN: Analyze requirements, list steps, estimate effort
EXECUTE: Implement each step, handle errors gracefully
VALIDATE: Run quality checks, verify outputs
REPORT: Summarize results, flag issues, suggest improvements

If validation fails, iterate: analyze the failure, adjust the plan, re-execute.
"""
```

### Multi-Day Project Example

**Day 1: Data Discovery**
- Catalog all source tables
- Profile data quality
- Map dependencies

**Day 2: Pipeline Design**
- Design ETL architecture
- Generate Terraform infrastructure
- Create Airflow DAGs

**Day 3: Implementation**
- Build extraction logic
- Implement transformations
- Set up loading process

**Day 4: Testing & Deployment**
- Run integration tests
- Deploy to staging
- Validate outputs
- Production release

---

## Key Patterns

### Pattern 1: Self-Correcting Pipeline
```
If the pipeline fails:
1. Analyze the error message
2. Identify root cause
3. Generate a fix
4. Re-run the failed step
5. Validate the fix
Maximum retries: 3
```

### Pattern 2: Parallel Execution
```
Execute in parallel:
- Thread 1: Extract from source A
- Thread 2: Extract from source B
- Thread 3: Fetch API metadata
Wait for all, then merge and transform.
```

### Pattern 3: Checkpoint & Resume
```
After each major step:
1. Save checkpoint to GCS
2. Log completion status
3. If interrupted, resume from last checkpoint
```

---

## Quiz

Complete the 10-question quiz in the interactive dashboard.

**Open the interactive module:** [index.html](./index.html)

---

*Next: [Module 05 - Evaluation & Runbooks](../05-Evaluation-Runbooks/)*
