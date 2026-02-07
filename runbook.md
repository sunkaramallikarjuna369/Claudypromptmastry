# ✅ Runbook: ClaudeOpus46-DataEng-Mastery

> Step-by-step guide from API setup to ETL demo to production deployment.

---

## Phase 1: Environment Setup

### Step 1.1 — Install Prerequisites

```bash
# Check Node.js version (need 18+)
node --version

# Check npm version
npm --version

# Install if needed (using nvm)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18
```

### Step 1.2 — Clone & Start

```bash
git clone https://github.com/sunkaramallikarjuna369/Claudypromptmastry.git
cd Claudypromptmastry
npm install
npm start
```

### Step 1.3 — Configure Anthropic API (Optional)

```bash
# Create environment file
echo 'VITE_ANTHROPIC_API_KEY=your-key-here' > .env.local

# Get your API key from:
# https://console.anthropic.com/settings/keys
```

> **Note:** The app works fully with mock APIs. Real API key is only needed for live Claude interactions.

---

## Phase 2: API Integration Options

### Option A — Anthropic Direct API

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Generate a PySpark ETL pipeline that reads from S3, transforms customer data, and writes to BigQuery."
        }
    ]
)
print(message.content[0].text)
```

### Option B — AWS Bedrock

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

response = bedrock.invoke_model(
    modelId='anthropic.claude-sonnet-4-20250514-v1:0',
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": "Create a Terraform module for a BigQuery dataset with partitioned tables."
            }
        ]
    })
)
result = json.loads(response['body'].read())
print(result['content'][0]['text'])
```

### Option C — Google Vertex AI

```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    region="us-east5",
    project_id="your-gcp-project"
)

message = client.messages.create(
    model="claude-sonnet-4@20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Write a Cloud Dataflow pipeline in Python for real-time event processing."
        }
    ]
)
print(message.content[0].text)
```

---

## Phase 3: ETL Demo Walkthrough

### Demo 1 — Pandas Data Cleaning with Claude

**Prompt Template:**
```
You are a senior data engineer. Analyze this CSV data and:
1. Identify all anomalies (nulls, outliers, format issues)
2. Generate a Pandas cleaning script with:
   - Null handling strategy (mean/median/mode per column type)
   - Outlier detection using IQR method
   - Date format standardization
   - String normalization
3. Add logging and error handling
4. Include unit tests

Data Schema:
- customer_id: INT (PK)
- email: VARCHAR(255)
- purchase_amount: DECIMAL(10,2)
- purchase_date: DATE
- region: VARCHAR(50)

Sample anomalies to handle:
- Null emails (5% of records)
- Negative purchase amounts
- Future dates
- Mixed case regions
```

### Demo 2 — Spark ETL Pipeline Generation

**Prompt Template:**
```
Generate a complete PySpark ETL pipeline with these specs:

SOURCE: S3 bucket (s3://raw-events/2024/)
- Format: Parquet, partitioned by date
- ~50GB daily, 500M records/month

TRANSFORMS:
1. Deduplicate on event_id
2. Parse nested JSON in 'metadata' column
3. Join with dim_customers (BigQuery)
4. Calculate rolling 7-day aggregates
5. Apply SCD Type 2 for customer dimensions

SINK: BigQuery dataset 'analytics.fact_events'
- Partitioned by event_date
- Clustered by customer_id, event_type

Include: Error handling, logging, data quality checks, unit tests
Optimize for: Memory efficiency, partition pruning
```

### Demo 3 — Terraform Infrastructure

**Prompt Template:**
```
Generate Terraform modules for a data engineering platform on GCP:

Resources needed:
1. BigQuery dataset with 3 tables (fact_events, dim_customers, dim_products)
2. Cloud Storage buckets (raw, staging, processed)
3. Dataflow job template
4. Cloud Composer (Airflow) environment
5. IAM roles and service accounts

Requirements:
- Use modules pattern (one module per resource type)
- Enable versioning on all buckets
- Set up lifecycle policies (90-day archive, 365-day delete)
- Configure BigQuery table partitioning and clustering
- Add monitoring alerts for pipeline failures
- Use variables for project_id, region, environment
```

---

## Phase 4: Agentic Workflow Setup

### Multi-Step Pipeline Agent

```python
AGENT_SYSTEM_PROMPT = """
You are a Data Engineering Agent. You have access to these tools:
1. execute_sql(query) - Run BigQuery SQL
2. run_python(code) - Execute Python/Pandas code
3. read_file(path) - Read data files
4. write_file(path, content) - Write output files
5. check_quality(dataset) - Run data quality checks

Your workflow for any data pipeline task:
PLAN → EXECUTE → VALIDATE → REPORT

For each step:
- Explain your reasoning
- Show the code/query
- Validate the output
- Handle errors gracefully
"""
```

---

## Phase 5: Production Deployment

### Deploy Checklist

- [ ] All mock APIs working correctly
- [ ] All 5 module quizzes functional
- [ ] Progress tracker saving to localStorage
- [ ] Mobile responsive layout verified
- [ ] GSAP animations performing at 60fps
- [ ] Code editors (CodeMirror) loading properly
- [ ] D3 visualizations rendering
- [ ] All navigation links working
- [ ] PWA manifest configured
- [ ] Deploy to Vercel/Netlify/Replit

### Deploy Commands

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Deploy to Vercel
npx vercel --prod

# Deploy to Netlify
npx netlify deploy --prod --dir=dist
```

---

## Phase 6: Evaluation Metrics

### Prompt Quality Scoring

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Code Correctness | >95% | Run generated code, check for errors |
| Completeness | >90% | All requested components present |
| Best Practices | >85% | Follows PEP8, includes error handling |
| Documentation | >80% | Docstrings, comments, README present |
| Performance | >75% | Efficient algorithms, proper indexing |

### Evaluation Prompt Template

```
Review the following Claude-generated code for a data engineering task.

Score on these dimensions (1-10):
1. CORRECTNESS: Does the code work as intended?
2. COMPLETENESS: Are all requirements addressed?
3. EFFICIENCY: Is the code optimized?
4. MAINTAINABILITY: Is the code clean and documented?
5. SECURITY: Are there any security concerns?

Provide:
- Overall score (weighted average)
- Top 3 strengths
- Top 3 areas for improvement
- Suggested fixes with code examples
```

---

*Last updated: February 2026*
