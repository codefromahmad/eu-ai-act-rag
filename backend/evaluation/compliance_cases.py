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
                "HR staff review recommendations "
                "before final hiring decisions."
            ),
        ),
    )


COMPLIANCE_CASES = [

    # --------------------------------------------------
    # REQ-009 — Risk Management
    # --------------------------------------------------

    {
        "name": "Risk management fully documented",
        "requirement_id": "REQ-009",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="risk_controls",
                value=(
                    "Continuous risk management process"
                ),
                page_number=3,
                quote=(
                    "The provider maintains a documented "
                    "continuous risk management process covering "
                    "risk identification, evaluation, mitigation, "
                    "testing and periodic review throughout "
                    "the system lifecycle."
                ),
            )
        ],
        "expected": ComplianceStatus.compliant,
    },

    {
        "name": "No risk management evidence",
        "requirement_id": "REQ-009",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },

    # --------------------------------------------------
    # REQ-010 — Data Governance
    # --------------------------------------------------

    {
        "name": "Data governance documented",
        "requirement_id": "REQ-010",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="training_data",
                value="Documented data governance",
                page_number=5,
                quote=(
                    "Training, validation and testing datasets "
                    "are documented, reviewed for relevance, "
                    "representativeness, data quality and "
                    "potential bias before model deployment."
                ),
            )
        ],
        "expected": ComplianceStatus.compliant,
    },

    {
        "name": "No data governance evidence",
        "requirement_id": "REQ-010",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },

    # --------------------------------------------------
    # REQ-011 — Technical Documentation
    # --------------------------------------------------

    {
        "name": "Technical documentation available",
        "requirement_id": "REQ-011",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="technical documentation",
                value="Technical documentation maintained",
                page_number=6,
                quote=(
                    "Technical documentation describing the "
                    "system architecture, intended purpose, "
                    "model design, validation procedures and "
                    "risk controls is maintained and updated."
                ),
            )
        ],
        "expected": ComplianceStatus.compliant,
    },

    {
        "name": "No technical documentation evidence",
        "requirement_id": "REQ-011",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },

    # --------------------------------------------------
    # REQ-012 — Record Keeping
    # --------------------------------------------------

    {
        "name": "Automatic logging implemented",
        "requirement_id": "REQ-012",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="logging",
                value="Automatic event logging",
                page_number=7,
                quote=(
                    "The system automatically records system "
                    "events, predictions, user actions and "
                    "administrative changes in audit logs."
                ),
            )
        ],
        "expected": ComplianceStatus.compliant,
    },

    {
        "name": "No logging evidence",
        "requirement_id": "REQ-012",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },

    # --------------------------------------------------
    # REQ-013 — Transparency
    # --------------------------------------------------

    {
        "name": "Transparency partially documented",
        "requirement_id": "REQ-013",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="transparency",
                value="Basic user information",
                page_number=8,
                quote=(
                    "HR users are informed that candidate "
                    "rankings are generated by an AI system "
                    "and are shown basic confidence scores."
                ),
            )
        ],
        "expected": ComplianceStatus.partial,
    },

    {
        "name": "No transparency evidence",
        "requirement_id": "REQ-013",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },

    # --------------------------------------------------
    # REQ-014 — Human Oversight
    # --------------------------------------------------

    {
        "name": "Human oversight partially documented",
        "requirement_id": "REQ-014",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="human_oversight",
                value="Human review before final decisions",
                page_number=9,
                quote=(
                    "HR staff review AI recommendations "
                    "before making the final hiring decision."
                ),
            )
        ],
        "expected": ComplianceStatus.partial,
    },

    {
        "name": "Human oversight strongly documented",
        "requirement_id": "REQ-014",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="human_oversight",
                value="Comprehensive human oversight",
                page_number=10,
                quote=(
                    "Trained HR staff review every AI result, "
                    "understand system limitations, monitor "
                    "for anomalies and automation bias, and "
                    "can disregard, override or stop the system."
                ),
            )
        ],
        "expected": ComplianceStatus.compliant,
    },

    # --------------------------------------------------
    # REQ-015 — Accuracy / Robustness / Cybersecurity
    # --------------------------------------------------

    {
        "name": "Accuracy and security partially documented",
        "requirement_id": "REQ-015",
        "profile": recruitment_profile(),
        "evidence": [
            ProfileEvidence(
                field="security",
                value="Accuracy and cybersecurity controls",
                page_number=11,
                quote=(
                    "The system is tested for accuracy and "
                    "uses access controls and encryption, "
                    "but robustness testing under adversarial "
                    "or failure conditions is not documented."
                ),
            )
        ],
        "expected": ComplianceStatus.partial,
    },

    {
        "name": "No accuracy robustness security evidence",
        "requirement_id": "REQ-015",
        "profile": recruitment_profile(),
        "evidence": [],
        "expected": ComplianceStatus.unknown,
    },
]