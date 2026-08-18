from pydantic import BaseModel, Field

from app.models.system_profile import SystemProfile


class ProfileEvidence(BaseModel):
    field: str
    value: str

    source_type: str = "section"

    source_number: int | None = None

    quote: str

    # Backward-compatible alias for older code/tests.
    @property
    def page_number(self) -> int | None:
        return self.source_number


class SystemProfileExtraction(BaseModel):
    profile: SystemProfile

    evidence: list[ProfileEvidence] = Field(
        default_factory=list
    )