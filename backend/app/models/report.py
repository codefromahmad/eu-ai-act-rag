from pydantic import BaseModel, Field

from app.models.analysis_result import AnalysisScore
from app.models.compliance import ComplianceAssessment
from app.models.risk_classification import RiskClassification


class ReportSummary(BaseModel):
    executive_summary: str

    strengths: list[str] = Field(
        default_factory=list
    )

    weaknesses: list[str] = Field(
        default_factory=list
    )

    missing_information: list[str] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )


class ComplianceReport(BaseModel):
    risk_classification: RiskClassification

    score: AnalysisScore

    summary: ReportSummary

    assessments: list[ComplianceAssessment]