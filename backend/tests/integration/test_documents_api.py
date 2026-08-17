from io import BytesIO
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.analysis_result import AnalysisScore
from app.models.report import (
    ComplianceReport,
    ReportSummary,
)
from app.models.risk_classification import (
    RiskCategory,
    RiskClassification,
)
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)


client = TestClient(app)


def test_extract_txt_document():

    content = (
        b"This AI system ranks job candidates.\n\n"
        b"HR staff review recommendations."
    )

    response = client.post(
        "/api/documents/extract",
        files={
            "file": (
                "system.txt",
                BytesIO(content),
                "text/plain",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "system.txt"
    assert data["file_type"] == "txt"
    assert data["section_count"] == 1
    assert data["page_count"] is None

    assert (
        "ranks job candidates"
        in data["text"]
    )


def test_extract_unsupported_file():

    response = client.post(
        "/api/documents/extract",
        files={
            "file": (
                "image.jpg",
                BytesIO(b"fake image"),
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        "Unsupported file type"
        in data["detail"]
    )


def test_extract_empty_file():

    response = client.post(
        "/api/documents/extract",
        files={
            "file": (
                "empty.txt",
                BytesIO(b""),
                "text/plain",
            )
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "The uploaded file is empty."
    }


def test_report_endpoint_with_mocked_pipeline():

    risk = RiskClassification(
        category=RiskCategory.high_risk,
        ai_act_applicable=True,
        explanation="Recruitment use.",
        relevant_articles=[
            "Article 6"
        ],
        relevant_annexes=[
            "Annex III"
        ],
        confidence=0.9,
    )

    score = AnalysisScore(
        compliance_score=50.0,
        coverage=14.29,
        total_requirements=7,
        known_requirements=1,
        compliant=0,
        partial=1,
        non_compliant=0,
        unknown=6,
    )

    report = ComplianceReport(
        risk_classification=risk,
        score=score,
        summary=ReportSummary(
            executive_summary="Mock compliance report.",
            strengths=[
                "Human oversight exists."
            ],
            weaknesses=[
                "Oversight controls are incomplete."
            ],
            missing_information=[
                "Risk management documentation."
            ],
            recommendations=[
                "Provide additional documentation."
            ],
        ),
        assessments=[],
    )

    profile = SystemProfile(
        system_purpose="AI recruitment system",
        intended_users=["HR staff"],
        domain="Employment",
        personal_data=True,
        automated_decisions=[
            "Candidate ranking"
        ],
        human_oversight=HumanOversight(
            present=True,
            description=(
                "HR reviews recommendations."
            ),
        ),
    )

    mock_result = {
        "analysis_id": "mock-analysis-id",
        "filename": "system.txt",
        "file_type": "txt",
        "page_count": None,
        "section_count": 1,
        "system_profile": profile,
        "user_evidence": [],
        "report": report,
    }

    with patch(
        "app.api.routes.documents."
        "CompliancePipelineService"
    ) as pipeline_class:

        pipeline_instance = (
            pipeline_class.return_value
        )

        pipeline_instance.analyze_document = (
            MagicMock(
                return_value=mock_result
            )
        )

        response = client.post(
            "/api/documents/report",
            files={
                "file": (
                    "system.txt",
                    BytesIO(
                        b"AI recruitment system"
                    ),
                    "text/plain",
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["analysis_id"]
        == "mock-analysis-id"
    )

    assert data["filename"] == "system.txt"
    assert data["file_type"] == "txt"

    assert (
        data["report"]["score"]
        ["compliance_score"]
        == 50.0
    )

    assert (
        data["report"]
        ["risk_classification"]
        ["category"]
        == "high_risk"
    )