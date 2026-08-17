from sqlalchemy.orm import Session

from app.models.analysis_result import (
    AnalysisScore,
    FullComplianceAnalysis,
)
from app.models.evidence import ProfileEvidence
from app.models.risk_classification import RiskCategory
from app.models.system_profile import SystemProfile
from app.services.compliance_analysis_service import (
    ComplianceAnalysisService,
)
from app.services.requirement_registry import REQUIREMENTS
from app.services.risk_classification_service import (
    RiskClassificationService,
)
from app.services.scoring_service import ScoringService


class FullAnalysisService:

    def __init__(self):
        self.compliance_service = ComplianceAnalysisService()
        self.risk_service = RiskClassificationService()
        self.scoring_service = ScoringService()

    def analyze(
        self,
        db: Session,
        profile: SystemProfile,
        user_evidence: list[ProfileEvidence],
    ) -> FullComplianceAnalysis:

        # 1. Classify the AI system first
        risk_classification = self.risk_service.classify(
            db=db,
            profile=profile,
        )

        # 2. Only run Articles 9–15 compliance analysis
        # when the system appears high-risk
        if risk_classification.category == RiskCategory.high_risk:

            assessments = (
                self.compliance_service.assess_all_requirements(
                    db=db,
                    profile=profile,
                    user_evidence=user_evidence,
                    requirements=REQUIREMENTS,
                )
            )

        else:
            assessments = []

        # 3. Calculate deterministic score
        score_data = self.scoring_service.calculate_score(
            assessments=assessments
        )

        score = AnalysisScore(
            **score_data
        )

        return FullComplianceAnalysis(
            risk_classification=risk_classification,
            assessments=assessments,
            score=score,
        )