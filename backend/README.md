# EU AI Act RAG Backend

Backend for an AI-assisted preliminary EU AI Act compliance assessment system.

## Main Features

- FastAPI backend
- PostgreSQL + pgvector
- EU AI Act knowledge base
- 114 Articles
- 13 Annexes
- Hybrid legal retrieval
- Cross-reference-aware retrieval
- Risk classification
- Requirement-level compliance assessment
- Compliance scoring
- Evidence coverage
- Structured compliance reports
- Analysis persistence
- PDF, DOCX, TXT and Markdown support
- Pytest unit and integration tests
- GitHub Actions CI

## Backend Flow

```text
Uploaded AI-system document
        ↓
Document validation
        ↓
Document extraction
        ↓
System profile extraction
        ↓
Evidence extraction
        ↓
Risk classification
        ↓
EU AI Act retrieval
        ↓
Compliance requirement analysis
        ↓
Compliance score + coverage
        ↓
Final compliance report
        ↓
PostgreSQL persistence
```

## Supported File Types

- PDF
- DOCX
- TXT
- Markdown

## EU AI Act Knowledge Base

The backend currently stores:

- 114 EU AI Act Articles
- 13 Annexes
- 127 embedded legal chunks

Legal embeddings are stored in PostgreSQL using pgvector.

## Main High-Risk Requirements

The current requirement registry includes:

- REQ-009 — Risk Management
- REQ-010 — Data and Data Governance
- REQ-011 — Technical Documentation
- REQ-012 — Record Keeping
- REQ-013 — Transparency
- REQ-014 — Human Oversight
- REQ-015 — Accuracy, Robustness and Cybersecurity

# Installation

## 1. Go to the backend directory

From the project root:

```bash
cd backend
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
```

## 3. Activate the virtual environment

On macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, the terminal should look similar to:

```text
(.venv) user@machine backend %
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

Then open:

```text
backend/.env
```

and configure:

```env
GROQ_API_KEY=your_real_groq_api_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=openai/gpt-oss-120b

DATABASE_URL=postgresql://your_username@localhost:5432/eu_ai_act_rag
```

Never commit the real `.env` file.

# PostgreSQL Setup

## 1. Make sure PostgreSQL is running

For a Homebrew installation on macOS, for example:

```bash
brew services start postgresql@14
```

The exact command may differ depending on the PostgreSQL version installed.

## 2. Create the database

```bash
createdb eu_ai_act_rag
```

## 3. Initialize database tables

From `backend/`:

```bash
python init_database.py
```

Expected output:

```text
Database tables created.
```

The initialization also enables the PostgreSQL `vector` extension when available.

# EU AI Act Knowledge Base

The source EU AI Act PDF is local project data and is not committed to GitHub.

Place the document at:

```text
backend/data/eu_ai_act.pdf
```

Then ingest it:

```bash
python ingest_eu_ai_act.py
```

Expected result:

```text
Ingested 127 legal chunks.
```

Verify the database:

```bash
python quick_test.py
```

Expected:

```text
Total chunks: 127
Chunks with embeddings: 127
```

# Run the Backend API

From the `backend/` directory:

```bash
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

# Main API Endpoints

```text
GET  /api/health

POST /api/documents/extract
POST /api/documents/analyze
POST /api/documents/report

GET  /api/analyses
GET  /api/analyses/{analysis_id}
```

## Document Extraction

```text
POST /api/documents/extract
```

Accepts:

- PDF
- DOCX
- TXT
- Markdown

and returns normalized document text and sections.

## Document Analysis

```text
POST /api/documents/analyze
```

Extracts:

- AI system profile
- intended purpose
- domain
- intended users
- automated decisions
- personal-data information
- human oversight
- supporting evidence

## Compliance Report

```text
POST /api/documents/report
```

Runs the complete pipeline:

```text
Document
→ profile extraction
→ evidence extraction
→ risk classification
→ EU AI Act retrieval
→ requirement analysis
→ scoring
→ report generation
→ database persistence
```

A successful response also contains an:

```text
analysis_id
```

which can later be used to retrieve the stored report.

# Testing

Run all backend tests:

```bash
pytest tests -v
```

Current automated test suite:

```text
19 tests passing
```

The test suite contains:

- unit tests
- API integration tests
- PostgreSQL integration tests
- document extraction tests
- validation tests
- mocked LLM pipeline tests

The same tests are automatically executed through GitHub Actions on pushes and pull requests to `main`.

# Evaluation

## Application-Aware Retrieval

Initial curated evaluation:

```text
8 / 8 cases passed
Accuracy: 100%
```

This includes important retrieval combinations such as:

```text
REQ-011
→ Article 11
→ Annex IV
```

and:

```text
Risk classification
→ Article 6
→ Annex III
```

This score applies only to the current curated evaluation dataset and should not be interpreted as general retrieval accuracy.

## Risk Classification

Initial completed real-model evaluation cases include:

- recruitment candidate ranking
- education admission scoring
- creditworthiness assessment

The completed cases have produced the expected high-risk classification.

Additional evaluation cases remain available for testing.

## Compliance Evaluation

The compliance evaluation framework tests:

- compliant
- partial
- non-compliant
- unknown

across the main high-risk requirements.

Some evaluation cases require live LLM calls and may be affected by provider usage limits.

# Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   ├── db/
│   │   └── models/
│   ├── exceptions/
│   ├── models/
│   ├── repositories/
│   └── services/
│       └── extractors/
│
├── evaluation/
├── tests/
│   ├── fixtures/
│   ├── integration/
│   └── unit/
│
├── data/
├── requirements.txt
├── init_database.py
└── ingest_eu_ai_act.py
```

# Important Disclaimer

This system performs an AI-assisted preliminary EU AI Act compliance assessment.

It is intended as a technical decision-support and analysis tool.

It is not a substitute for professional legal advice and should not be treated as a definitive legal determination.
