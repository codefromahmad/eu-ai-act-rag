from app.models.compliance import ComplianceStatus
from app.models.evidence import ProfileEvidence
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)


COMPLIANCE_CASES = [
    {
        "name": "Human oversight partially documented",

        "requirement_id": "REQ-014",

        "profile": SystemProfile(
            system_purpose="AI-assisted recruitment system",
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
                    "before final hiring decisions."
                ),
            ),
        ),

        "evidence": [
            ProfileEvidence(
                field="human_oversight",
                value=(
                    "HR review before final decisions"
                ),
                page_number=4,
                quote=(
                    "HR staff review AI recommendations "
                    "before making the final hiring decision."
                ),
            )
        ],

        "expected": ComplianceStatus.partial,
    },

    {
        "name": "No risk management evidence",

        "requirement_id": "REQ-009",

        "profile": SystemProfile(
            system_purpose="AI-assisted recruitment system",
            intended_users=["HR staff"],
            domain="Employment",
            personal_data=True,
            automated_decisions=[
                "Candidate ranking"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "HR reviews recommendations."
                ),
            ),
        ),

        "evidence": [],

        "expected": ComplianceStatus.unknown,
    },

    {
        "name": "No technical documentation evidence",

        "requirement_id": "REQ-011",

        "profile": SystemProfile(
            system_purpose="AI-assisted recruitment system",
            intended_users=["HR staff"],
            domain="Employment",
            personal_data=True,
            automated_decisions=[
                "Candidate ranking"
            ],
            human_oversight=HumanOversight(
                present=True,
                description=(
                    "HR reviews recommendations."
                ),
            ),
        ),

        "evidence": [],

        "expected": ComplianceStatus.unknown,
    },
]