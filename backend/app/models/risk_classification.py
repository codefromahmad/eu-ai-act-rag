from enum import Enum

from pydantic import BaseModel, Field


class RiskCategory(str, Enum):
    prohibited = "prohibited"
    high_risk = "high_risk"
    limited_risk = "limited_risk"
    minimal_risk = "minimal_risk"
    uncertain = "uncertain"


class RiskClassification(BaseModel):
    category: RiskCategory

    ai_act_applicable: bool | None = None

    explanation: str

    relevant_articles: list[str] = Field(
        default_factory=list
    )

    relevant_annexes: list[str] = Field(
        default_factory=list
    )

    indicators: list[str] = Field(
        default_factory=list
    )

    missing_information: list[str] = Field(
        default_factory=list
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )