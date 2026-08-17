from app.models.system_profile import (
    HumanOversight,
    ModelInfo,
    SystemProfile,
)


profile = SystemProfile(
    system_purpose="AI-powered recruitment system",
    intended_users=["HR departments"],
    domain="Employment",
    deployment_context="Enterprise",
    models=[
        ModelInfo(
            name="Example LLM",
            provider="Example Provider",
            model_type="LLM",
        )
    ],
    data_types=["CVs", "Candidate information"],
    personal_data=True,
    automated_decisions=[
        "Candidate ranking",
    ],
    human_oversight=HumanOversight(
        present=True,
        description="HR reviews recommendations before final decisions.",
    ),
    unknown_information=[
        "Monitoring procedure is not described.",
    ],
)

print(profile.model_dump())