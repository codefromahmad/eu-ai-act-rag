from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    name: str | None = None
    provider: str | None = None
    model_type: str | None = None


class HumanOversight(BaseModel):
    present: bool | None = None
    description: str | None = None


class SystemProfile(BaseModel):
    system_purpose: str | None = None

    intended_users: list[str] = Field(default_factory=list)

    domain: str | None = None

    deployment_context: str | None = None

    models: list[ModelInfo] = Field(default_factory=list)

    data_types: list[str] = Field(default_factory=list)

    personal_data: bool | None = None

    automated_decisions: list[str] = Field(default_factory=list)

    human_oversight: HumanOversight | None = None

    risk_controls: list[str] = Field(default_factory=list)

    monitoring: str | None = None

    security: str | None = None

    transparency: str | None = None

    unknown_information: list[str] = Field(default_factory=list)