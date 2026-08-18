from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.models.risk_classification import RiskCategory


RISK_CLASSIFICATION_CASES = [
    {
        "name": "Recruitment candidate ranking",
        "profile": SystemProfile(
            system_purpose=(
                "AI system used to rank job applicants "
                "during recruitment."
            ),
            intended_users=["HR staff"],
            domain="Employment",
            personal_data=True,
            automated_decisions=[
                "Candidate ranking"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "HR staff review recommendations "
                    "before final decisions."
                ),
            ),
        ),
        "expected": RiskCategory.high_risk,
    },

    {
        "name": "Education admission scoring",
        "profile": SystemProfile(
            system_purpose=(
                "AI system used to score applicants "
                "for university admission."
            ),
            intended_users=[
                "University admission staff"
            ],
            domain="Education",
            personal_data=True,
            automated_decisions=[
                "Admission scoring"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "Admission staff review results."
                ),
            ),
        ),
        "expected": RiskCategory.high_risk,
    },

    {
        "name": "Creditworthiness assessment",
        "profile": SystemProfile(
            system_purpose=(
                "AI system used to assess whether "
                "individuals are creditworthy."
            ),
            intended_users=[
                "Bank employees"
            ],
            domain="Financial services",
            personal_data=True,
            automated_decisions=[
                "Creditworthiness assessment"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "Bank staff can review decisions."
                ),
            ),
        ),
        "expected": RiskCategory.high_risk,
    },

    {
        "name": "Simple email spam filter",
        "profile": SystemProfile(
            system_purpose=(
                "AI system that identifies and filters "
                "spam emails."
            ),
            intended_users=[
                "Email users"
            ],
            domain="Email",
            personal_data=False,
            automated_decisions=[
                "Spam classification"
            ],
            human_oversight=HumanOversight(
                present=False,
                description=None,
            ),
        ),
        "expected": RiskCategory.minimal_risk,
    },

    {
        "name": "Insufficient system description",
        "profile": SystemProfile(
            system_purpose="AI-powered system",
            intended_users=[],
            domain=None,
            personal_data=False,
            automated_decisions=[],
            human_oversight=HumanOversight(
                present=False,
                description=None,
            ),
        ),
        "expected": RiskCategory.uncertain,
    },
]