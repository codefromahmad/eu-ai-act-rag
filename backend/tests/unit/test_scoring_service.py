from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
)
from app.services.scoring_service import ScoringService


def test_scoring_service_calculates_score_and_coverage():

    assessments = [
        ComplianceAssessment(
            requirement_id="REQ-009",
            status=ComplianceStatus.compliant,
            explanation="Risk management is documented.",
        ),
        ComplianceAssessment(
            requirement_id="REQ-010",
            status=ComplianceStatus.partial,
            explanation="Some controls are documented.",
        ),
        ComplianceAssessment(
            requirement_id="REQ-011",
            status=ComplianceStatus.non_compliant,
            explanation="Technical documentation is missing.",
        ),
        ComplianceAssessment(
            requirement_id="REQ-012",
            status=ComplianceStatus.unknown,
            explanation="Insufficient information.",
        ),
    ]

    service = ScoringService()

    result = service.calculate_score(
        assessments=assessments
    )

    assert result["compliance_score"] == 50.0
    assert result["coverage"] == 75.0
    assert result["total_requirements"] == 4
    assert result["known_requirements"] == 3
    assert result["compliant"] == 1
    assert result["partial"] == 1
    assert result["non_compliant"] == 1
    assert result["unknown"] == 1