# Module 05: Evaluation & Runbooks

> **What** metrics should you use to evaluate Claude's data engineering output?
> **Who** is responsible for quality assurance in AI-assisted pipelines?
> **When** should you evaluate — during development or in production?
> **Where** do evaluation frameworks fit in the SDLC?
> **How** do you build effective evaluation dashboards and runbooks?

---

## Overview

This module teaches you to measure, evaluate, and continuously improve Claude's performance on data engineering tasks. Build production runbooks and metrics dashboards.

### Evaluation Dimensions

| Dimension | Weight | What to Measure |
|-----------|--------|----------------|
| Correctness | 30% | Does the generated code run without errors? |
| Completeness | 25% | Are all requirements addressed? |
| Efficiency | 20% | Is the code optimized for performance? |
| Maintainability | 15% | Is the code clean, documented, testable? |
| Security | 10% | Are credentials and data handled safely? |

### Scoring Framework

```
EVALUATION PROMPT:
Review the following Claude-generated {artifact_type}:

{code_or_config}

Score each dimension (1-10):
1. CORRECTNESS: Does it work as intended?
2. COMPLETENESS: Are all requirements met?
3. EFFICIENCY: Is it optimized?
4. MAINTAINABILITY: Is it clean and documented?
5. SECURITY: Are there security concerns?

Calculate weighted score:
Overall = (C1*0.3) + (C2*0.25) + (C3*0.2) + (C4*0.15) + (C5*0.1)

Provide:
- Overall score with interpretation
- Top 3 strengths
- Top 3 improvement areas
- Specific code fixes for any score < 7
```

### Quality Targets

| Metric | Minimum | Target | Excellent |
|--------|---------|--------|-----------|
| Code Correctness | 70% | 90% | 98% |
| Test Pass Rate | 80% | 95% | 100% |
| Prompt Success Rate | 60% | 85% | 95% |
| Time Saved vs Manual | 2x | 5x | 10x |

---

## Production Runbook Template

### Runbook: Daily ETL Pipeline

**Purpose:** Process daily transactional data through Claude-assisted ETL

**Schedule:** Daily at 02:00 UTC

**Steps:**
1. **Pre-flight Check**
   - Verify source data availability
   - Check BigQuery quotas
   - Validate Claude API health

2. **Extract**
   - Pull data from sources
   - Log record counts
   - Validate schema consistency

3. **Transform (Claude-Assisted)**
   - Send data profile to Claude
   - Apply generated cleaning rules
   - Execute transformations
   - Log transformation metrics

4. **Load**
   - Write to BigQuery staging
   - Run quality checks
   - Promote to production tables

5. **Post-Validation**
   - Compare row counts (source vs target)
   - Check for null rates
   - Validate business rules
   - Send alerts if thresholds breached

**Rollback Procedure:**
1. Identify failed step from logs
2. Restore from last good checkpoint
3. Re-run from failed step with fixes
4. Validate and promote

---

## Quiz

Complete the 10-question quiz in the interactive dashboard.

**Open the interactive module:** [runbook.html](./runbook.html)

---

*Congratulations! You've completed all 5 modules!*
