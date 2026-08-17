from pydantic import BaseModel

from app.models.compliance import ComplianceAssessment


class AnalysisScore(BaseModel):
    compliance_score: float | None
    coverage: float
    total_requirements: int
    known_requirements: int
    compliant: int
    partial: int
    non_compliant: int
    unknown: int


class FullComplianceAnalysis(BaseModel):
    assessments: list[ComplianceAssessment]
    score: AnalysisScore