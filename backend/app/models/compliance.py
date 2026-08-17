from enum import Enum

from pydantic import BaseModel, Field


class ComplianceStatus(str, Enum):
    compliant = "compliant"
    partial = "partial"
    non_compliant = "non_compliant"
    unknown = "unknown"


class LegalReference(BaseModel):
    article: str
    text: str


class ComplianceRequirement(BaseModel):
    requirement_id: str

    title: str

    description: str

    query: str

    legal_references: list[LegalReference] = Field(
        default_factory=list
    )


class ComplianceAssessment(BaseModel):
    requirement_id: str

    status: ComplianceStatus

    explanation: str

    user_evidence: list[str] = Field(
        default_factory=list
    )

    legal_references: list[LegalReference] = Field(
        default_factory=list
    )

    recommendations: list[str] = Field(
        default_factory=list
    )