# EU AI Act Compliance Analyzer

An evidence-grounded RAG system for analyzing AI system documentation against relevant requirements of the **EU AI Act**.

The application accepts technical documentation describing an AI system, extracts a structured system profile, determines the applicable AI Act risk category, retrieves relevant legal provisions, evaluates available evidence against compliance requirements, and generates an explainable compliance assessment.

> **Disclaimer:** This project is an AI-assisted compliance assessment and decision-support tool. It does not provide legal advice or constitute a formal determination of EU AI Act compliance.

---

## Overview

Organizations developing or deploying AI systems may need to understand which EU AI Act obligations apply to their systems and whether their existing documentation provides sufficient evidence of compliance.

This project explores how **Retrieval-Augmented Generation (RAG), structured information extraction, semantic retrieval, and LLM-based reasoning** can support that process.

Instead of asking an LLM to evaluate a document against the entire regulation directly, the system uses a structured pipeline:

1. Validate and extract the uploaded document.
2. Convert the document into a structured AI system profile.
3. Preserve evidence supporting extracted facts.
4. Classify the AI system under the EU AI Act risk framework.
5. Identify relevant compliance requirements.
6. Retrieve corresponding EU AI Act provisions.
7. Match user evidence to individual requirements.
8. Evaluate each requirement independently.
9. Calculate compliance and evidence-coverage scores.
10. Generate and persist an explainable report.

---

## Key Features

- Upload AI system documentation in **PDF, DOCX, Markdown, or TXT**
- Structured AI system profile extraction using an LLM
- Evidence-grounded extraction with source references
- EU AI Act risk classification
- Retrieval of relevant Articles and Annexes
- Requirement-specific evidence selection
- Compliance assessment per requirement
- Four assessment states:
  - `compliant`
  - `partial`
  - `non_compliant`
  - `unknown`
- Separate compliance and evidence-coverage scoring
- Explainable findings with user and legal evidence
- Actionable recommendations
- PostgreSQL persistence for generated analyses
- Analysis history and saved-report retrieval
- REST API built with FastAPI
- Modern React dashboard for report visualization
- Automated unit and integration testing
- CI-ready project structure

---

## System Architecture

```text
                         ┌──────────────────────────┐
                         │       React Client       │
                         │    React + Tailwind CSS  │
                         └────────────┬─────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌──────────────────────────┐
                         │        FastAPI API       │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │   Document Validation    │
                         │ PDF / DOCX / TXT / MD    │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │  Document Extraction     │
                         │ pages / sections / text  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ System Profile + Evidence│
                         │          LLM             │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │    Risk Classification   │
                         └────────────┬─────────────┘
                                      │
                         ┌────────────┴─────────────┐
                         │                          │
                         ▼                          ▼
              ┌────────────────────┐    ┌─────────────────────┐
              │ Requirement        │    │ EU AI Act Retrieval │
              │ Registry           │    │ Articles / Annexes  │
              └─────────┬──────────┘    └──────────┬──────────┘
                        │                          │
                        └────────────┬─────────────┘
                                     ▼
                         ┌──────────────────────────┐
                         │   Evidence Selection     │
                         │ requirement ↔ evidence   │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ Compliance Assessment    │
                         │ compliant / partial /    │
                         │ non-compliant / unknown  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ Scoring + Report         │
                         │ compliance + coverage    │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │ PostgreSQL + pgvector    │
                         │ analyses + legal corpus  │
                         └──────────────────────────┘
```

---

## Why Evidence Grounding?

A major design goal of the project is to avoid treating an LLM response as sufficient evidence.

The pipeline therefore distinguishes between two types of evidence.

### User Evidence

Evidence extracted directly from the AI system documentation uploaded by the user.

Example:

```text
HR staff review AI-generated recommendations and can override rankings.
```

### Legal Evidence

Relevant provisions retrieved from the EU AI Act knowledge base.

Example:

```text
Article 14 — Human Oversight
```

The compliance analyzer evaluates the relevant user evidence against the corresponding legal requirement instead of comparing every document statement against every Article.

This reduces unnecessary LLM calls and makes assessments more traceable.

---

## Compliance Assessment

Applicable requirements are evaluated independently.

| Status            | Meaning                                                             |
| ----------------- | ------------------------------------------------------------------- |
| **Compliant**     | Available evidence sufficiently demonstrates the requirement        |
| **Partial**       | Some evidence exists, but the requirement is not fully demonstrated |
| **Non-compliant** | Evidence indicates that the requirement is not satisfied            |
| **Unknown**       | The uploaded documentation does not provide enough evidence         |

`Unknown` is intentionally different from `Non-compliant`.

Missing documentation should not automatically be interpreted as proof that a system violates a legal requirement.

---

## Compliance Score vs Evidence Coverage

The project separates two concepts that are often incorrectly combined.

### Compliance Score

Measures performance across requirements for which sufficient evidence was available.

### Evidence Coverage

Measures how much of the applicable compliance framework could actually be assessed from the uploaded documentation.

For example:

```text
Compliance Score: 50%
Evidence Coverage: 14.29%
```

A moderate compliance score with very low coverage should therefore **not** be interpreted as strong overall compliance.

This distinction makes uncertainty visible to the user.

---

## Example Use Case

Consider an AI recruitment system that:

- analyzes candidate profiles
- generates candidate rankings
- processes applicant personal data
- provides recommendations to HR staff
- allows HR staff to override AI recommendations

The pipeline can identify recruitment as a potentially **high-risk AI use case**, retrieve the relevant EU AI Act requirements, and evaluate whether the uploaded documentation contains evidence for areas such as:

- risk management
- data governance
- technical documentation
- record keeping
- transparency
- human oversight
- accuracy, robustness, and cybersecurity

The resulting report highlights strengths, weaknesses, missing information, and recommended actions.

---

## Technology Stack

### Backend

- Python 3.11
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- pgvector
- PyMuPDF
- python-docx
- Sentence Transformers
- Groq-hosted LLM
- pytest

### Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React

### AI / Retrieval

- Large Language Models
- Retrieval-Augmented Generation
- Semantic embeddings
- Vector similarity search
- Hybrid legal retrieval
- Structured JSON extraction
- Evidence-grounded compliance reasoning

---

## Project Structure

```text
eu-ai-act-rag/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   └── services/
│   │
│   ├── evaluation/
│   ├── tests/
│   │   ├── integration/
│   │   └── unit/
│   │
│   ├── ARCHITECTURE.md
│   ├── README.md
│   └── .env.example
│
├── frontend/
│   ├── public/
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
│
└── README.md
```

---

## Backend Pipeline

The main analysis pipeline follows:

```text
Uploaded Document
       ↓
File Validation
       ↓
Document Extraction
       ↓
System Profile Extraction
       ↓
User Evidence Extraction
       ↓
Risk Classification
       ↓
Requirement Selection
       ↓
EU AI Act Retrieval
       ↓
Requirement-specific Evidence Selection
       ↓
Compliance Analysis
       ↓
Scoring
       ↓
Report Generation
       ↓
PostgreSQL Persistence
```

---

## API

### Generate Compliance Report

```http
POST /api/documents/report
```

Accepts an uploaded AI system document and executes the complete compliance pipeline.

### Extract Document

```http
POST /api/documents/extract
```

Validates and extracts supported documents.

### Analysis History

```http
GET /api/analyses
```

Returns stored analyses.

### Analysis Detail

```http
GET /api/analyses/{analysis_id}
```

Returns a previously generated analysis.

### Health

```http
GET /api/health
```

### Readiness

```http
GET /api/ready
```

---

## Local Development

### 1. Clone

```bash
git clone https://github.com/codefromahmad/eu-ai-act-rag.git
cd eu-ai-act-rag
```

### 2. Backend

```bash
cd backend

python3.11 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create the environment configuration:

```bash
cp .env.example .env
```

Configure the required database and LLM credentials in `.env`.

Start the backend:

```bash
python -m uvicorn app.main:app --reload
```

The FastAPI server runs locally on:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 3. Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server runs locally on:

```text
http://localhost:5173
```

---

## Testing

The backend includes unit and integration tests covering major parts of the application.

Run:

```bash
cd backend
source .venv/bin/activate
pytest tests -v
```

Current test suite:

```text
23 passed
```

Coverage includes:

- document validation
- document extraction
- evidence selection
- compliance analysis
- scoring
- pipeline orchestration
- document API behavior
- analysis persistence API
- health/readiness endpoints
- API error handling
- LLM quota exhaustion handling

---

## Frontend Production Build

```bash
cd frontend
npm run build
```

The frontend is production-buildable using Vite.

---

## Reliability and Safety Considerations

The project intentionally includes several safeguards:

- missing information is represented explicitly
- unsupported evidence is not fabricated
- user evidence retains source references
- legal evidence remains traceable to EU AI Act provisions
- requirements are evaluated independently
- evidence coverage is separated from compliance score
- external LLM quota failures are handled by the API
- file type and size validation occur before analysis

---

## Limitations

This is a portfolio and research-oriented implementation rather than a certified legal compliance product.

Current limitations include:

- LLM outputs can still contain reasoning errors
- retrieval quality depends on the indexed legal corpus
- compliance interpretation can require legal expertise
- uploaded documentation may omit important operational information
- a high compliance score with low evidence coverage should not be treated as proof of compliance
- regulatory guidance and interpretation may evolve
- external LLM services introduce availability and quota dependencies

Future production systems would require additional legal review, security hardening, privacy controls, evaluation, auditability, and regulatory-change management.

---

## Application Screenshots

### Analyze an AI System

Upload AI system documentation and start an evidence-grounded EU AI Act compliance assessment.

![Document Analysis](docs/screenshots/home.png)

### Compliance Report

The generated report presents the system's risk classification, compliance score, evidence coverage, strengths, weaknesses, missing information, and recommendations.

![Compliance Report](docs/screenshots/report.png)

### Requirement-Level Assessment

Each applicable requirement is assessed independently using evidence from the uploaded documentation and retrieved EU AI Act provisions. Legal references can be expanded for traceability.

![Requirement and Legal Evidence](docs/screenshots/legal-reference.png)

### Analysis History

Completed analyses are persisted in PostgreSQL and can be reopened without running the LLM pipeline again.

![Analysis History](docs/screenshots/history.png)

---

## Future Improvements

Potential extensions include:

- stronger retrieval evaluation
- citation-level legal traceability
- provider/deployer-specific obligation analysis
- additional EU AI Act risk categories and obligations
- regulatory knowledge-base versioning
- asynchronous analysis jobs
- authentication and multi-user workspaces
- PDF report export
- configurable LLM providers
- richer evaluation datasets
- deployment monitoring and observability

---

## Author

**Aafaq Ahmad**

Software Engineering / NLP / AI Engineering

GitHub: `@codefromahmad`

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

This software is provided for educational, research, and portfolio purposes.

The generated assessments are informational and should not be interpreted as legal advice, certification, or a definitive determination of compliance with Regulation (EU) 2024/1689 or any other applicable law.
