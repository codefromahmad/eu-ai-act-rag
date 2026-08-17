from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
)
from app.services.scoring_service import ScoringService


assessments = [
    ComplianceAssessment(
        requirement_id="REQ-009",
        status=ComplianceStatus.compliant,
        explanation="Risk management is documented.",
    ),

    ComplianceAssessment(
        requirement_id="REQ-010",
        status=ComplianceStatus.partial,
        explanation="Some data governance controls exist.",
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

print(result)