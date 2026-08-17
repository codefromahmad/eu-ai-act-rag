from sqlalchemy.orm import Session

from app.models.analysis_result import (
    AnalysisScore,
    FullComplianceAnalysis,
)
from app.models.evidence import ProfileEvidence
from app.models.system_profile import SystemProfile
from app.services.compliance_analysis_service import (
    ComplianceAnalysisService,
)
from app.services.requirement_registry import REQUIREMENTS
from app.services.scoring_service import ScoringService


class FullAnalysisService:

    def __init__(self):
        self.compliance_service = ComplianceAnalysisService()
        self.scoring_service = ScoringService()

    def analyze(
        self,
        db: Session,
        profile: SystemProfile,
        user_evidence: list[ProfileEvidence],
    ) -> FullComplianceAnalysis:

        assessments = (
            self.compliance_service.assess_all_requirements(
                db=db,
                profile=profile,
                user_evidence=user_evidence,
                requirements=REQUIREMENTS,
            )
        )

        score_data = self.scoring_service.calculate_score(
            assessments=assessments
        )

        score = AnalysisScore(
            **score_data
        )

        return FullComplianceAnalysis(
            assessments=assessments,
            score=score,
        )