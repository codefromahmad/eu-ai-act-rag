from pydantic import BaseModel, Field

from app.models.system_profile import SystemProfile


class ProfileEvidence(BaseModel):
    field: str
    value: str
    page_number: int
    quote: str


class SystemProfileExtraction(BaseModel):
    profile: SystemProfile

    evidence: list[ProfileEvidence] = Field(
        default_factory=list
    )