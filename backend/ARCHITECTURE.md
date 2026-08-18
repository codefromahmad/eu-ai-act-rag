# Backend Architecture

## Overview

The backend is a FastAPI-based EU AI Act compliance assessment system.

Its main purpose is to analyze documentation describing an AI system, classify its regulatory risk, retrieve relevant EU AI Act provisions, assess compliance requirements, calculate a score, and generate a structured report.

## High-Level Flow

```text
Uploaded Document
        ↓
File Validation
        ↓
Document Extraction
        ↓
System Profile Extraction
        ↓
Evidence Extraction
        ↓
Risk Classification
        ↓
Legal Retrieval
        ↓
Requirement Assessment
        ↓
Scoring
        ↓
Report Generation
        ↓
PostgreSQL Persistence
```

## 1. API Layer

Location:

```text
app/api/routes/
```

Main routes:

```text
health.py
documents.py
analyses.py
```

Responsibilities:

- receive HTTP requests
- validate request-level input
- return HTTP responses
- translate internal exceptions into API errors

The API layer should not contain core compliance logic.

## 2. Document Input Layer

Main services:

```text
FileValidationService
DocumentExtractionService
```

Supported formats:

- PDF
- DOCX
- TXT
- Markdown

Individual extractors are located in:

```text
app/services/extractors/
```

They convert different file formats into one normalized `ExtractedDocument` structure.

## 3. System Profile Extraction

Main service:

```text
SystemProfileService
```

The service converts the extracted document into a structured description of the AI system.

Example fields include:

- system purpose
- domain
- intended users
- personal data usage
- automated decisions
- human oversight

The service also extracts supporting evidence from the submitted documentation.

## 4. EU AI Act Knowledge Base

The legal knowledge base contains:

```text
114 Articles
13 Annexes
127 legal chunks
```

Legal chunks are stored in PostgreSQL.

Embeddings are stored using pgvector.

Each legal chunk can contain:

- article
- annex
- heading
- legal text
- source
- version
- embedding

## 5. Retrieval Layer

The backend uses several retrieval strategies.

### Generic Hybrid Retrieval

```text
RetrievalService
```

Combines semantic and keyword-oriented retrieval.

### Requirement Retrieval

```text
RequirementRetrievalService
```

Retrieves legal evidence for specific compliance requirements.

It also expands explicit legal cross-references.

Example:

```text
Article 11
→ Annex IV
```

### Classification Retrieval

```text
ClassificationRetrievalService
```

Provides the core legal sources needed for risk classification.

Example:

```text
Article 6
+
Annex III
```

## 6. Risk Classification

Main service:

```text
RiskClassificationService
```

The system first determines the likely EU AI Act risk category before running detailed compliance checks.

Possible categories include:

- prohibited
- high_risk
- limited_risk
- minimal_risk
- uncertain

The classifier is grounded using retrieved legal evidence.

## 7. Compliance Requirements

The current requirement registry focuses on key high-risk AI obligations:

```text
REQ-009 — Risk Management
REQ-010 — Data and Data Governance
REQ-011 — Technical Documentation
REQ-012 — Record Keeping
REQ-013 — Transparency
REQ-014 — Human Oversight
REQ-015 — Accuracy, Robustness and Cybersecurity
```

## 8. Evidence-Aware Compliance Analysis

Main services:

```text
EvidenceSelectionService
ComplianceAnalysisService
```

The evidence-selection layer first determines whether the user document contains evidence relevant to a requirement.

If no relevant evidence exists:

```text
status = unknown
```

and no LLM call is required.

If relevant evidence exists, the LLM evaluates it against retrieved legal evidence.

Possible statuses:

- compliant
- partial
- non_compliant
- unknown

## 9. Scoring

Main service:

```text
ScoringService
```

The scoring layer is deterministic.

It calculates:

- compliance score
- evidence coverage
- number of compliant requirements
- partial requirements
- non-compliant requirements
- unknown requirements

The LLM does not generate the final score.

## 10. Report Generation

Main service:

```text
ReportService
```

The report contains:

- risk classification
- compliance score
- evidence coverage
- executive summary
- strengths
- weaknesses
- missing information
- recommendations
- detailed assessments
- legal references

The report-generation LLM receives summarized findings rather than repeatedly receiving full legal text.

## 11. Pipeline Orchestration

Main service:

```text
CompliancePipelineService
```

This service coordinates the full workflow:

```text
Document
→ extraction
→ profile
→ evidence
→ classification
→ compliance analysis
→ score
→ report
→ persistence
```

This keeps the FastAPI routes relatively thin.

## 12. Persistence

Main database tables:

```text
legal_chunks
analyses
```

`legal_chunks` stores the EU AI Act knowledge base.

`analyses` stores completed compliance analyses, including:

- analysis ID
- filename
- file type
- risk category
- compliance score
- coverage
- system profile
- report
- creation timestamp

## 13. LLM Layer

Main service:

```text
LLMService
```

The backend currently uses a Groq-compatible OpenAI API interface.

Custom exception handling covers:

- temporary rate limits
- quota exhaustion
- invalid responses
- provider errors

The design keeps LLM-related behavior centralized.

## 14. Testing

Tests are organized into:

```text
tests/unit/
tests/integration/
```

Current automated suite:

```text
19 tests
```

Tests cover:

- scoring
- evidence selection
- file validation
- document extraction
- compliance orchestration
- persistence
- FastAPI endpoints

GitHub Actions runs the test suite automatically.

## 15. Evaluation

The project contains dedicated evaluation scripts for:

- generic retrieval
- application-aware retrieval
- risk classification
- compliance classification

Initial application-aware retrieval evaluation:

```text
8 / 8 curated cases passed
```

This result applies only to the current small evaluation dataset.

## Design Principle

The backend separates:

```text
Deterministic application logic
```

from:

```text
LLM reasoning
```

and from:

```text
legal retrieval
```

This makes the system easier to test, debug, evaluate and extend.
