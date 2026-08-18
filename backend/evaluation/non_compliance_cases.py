from app.models.compliance import ComplianceStatus
from app.models.evidence import ProfileEvidence
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)


def recruitment_profile() -> SystemProfile:
    return SystemProfile(
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
                "HR staff use AI recommendations "
                "during recruitment."
            ),
        ),
    )


NON_COMPLIANCE_CASES = [

    # --------------------------------------------------
    # REQ-012 — Record Keeping
    # --------------------------------------------------

    {
        "name": "Logging explicitly not implemented",

        "requirement_id": "REQ-012",

        "profile": recruitment_profile(),

        "evidence": [
            ProfileEvidence(
                field="logging",
                value="Logging is disabled",
                page_number=12,
                quote=(
                    "The system does not automatically "
                    "generate or retain logs of predictions, "
                    "system events, or user actions."
                ),
            )
        ],

        "expected": ComplianceStatus.non_compliant,
    },

    # --------------------------------------------------
    # REQ-014 — Human Oversight
    # --------------------------------------------------

    {
        "name": "Human decisions cannot override AI",

        "requirement_id": "REQ-014",

        "profile": SystemProfile(
            system_purpose="AI recruitment system",
            intended_users=["HR staff"],
            domain="Employment",
            personal_data=True,
            automated_decisions=[
                "Automatic candidate rejection"
            ],
            human_oversight=HumanOversight(
                present=False,
                description=(
                    "Candidate decisions are made "
                    "automatically."
                ),
            ),
        ),

        "evidence": [
            ProfileEvidence(
                field="human_oversight",
                value="No human override",
                page_number=13,
                quote=(
                    "Candidate rejection decisions are "
                    "performed automatically and HR staff "
                    "cannot override or stop the decision."
                ),
            )
        ],

        "expected": ComplianceStatus.non_compliant,
    },

    # --------------------------------------------------
    # REQ-015 — Accuracy / Robustness / Cybersecurity
    # --------------------------------------------------

    {
        "name": "Security safeguards explicitly absent",

        "requirement_id": "REQ-015",

        "profile": recruitment_profile(),

        "evidence": [
            ProfileEvidence(
                field="security",
                value="No cybersecurity controls",
                page_number=14,
                quote=(
                    "The system has not undergone robustness "
                    "or cybersecurity testing and currently "
                    "does not implement access controls, "
                    "security monitoring, or protections "
                    "against adversarial manipulation."
                ),
            )
        ],

        "expected": ComplianceStatus.non_compliant,
    },
]