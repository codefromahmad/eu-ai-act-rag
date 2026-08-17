from app.models.compliance import ComplianceRequirement


REQUIREMENTS = [
    ComplianceRequirement(
        requirement_id="REQ-009",
        title="Risk Management",
        description=(
            "The AI system should implement an appropriate "
            "risk management process."
        ),
        query="risk management system requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-010",
        title="Data and Data Governance",
        description=(
            "Training, validation and testing data should meet "
            "appropriate data governance and quality requirements."
        ),
        query="training validation testing data governance requirements",
    ),

    ComplianceRequirement(
        requirement_id="REQ-011",
        title="Technical Documentation",
        description=(
            "The system should have sufficient technical documentation."
        ),
        query="technical documentation requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-012",
        title="Record Keeping",
        description=(
            "The system should support appropriate logging "
            "and record keeping."
        ),
        query="automatic logging and record keeping requirements",
    ),

    ComplianceRequirement(
        requirement_id="REQ-013",
        title="Transparency",
        description=(
            "Deployers should receive sufficient information "
            "to understand and use the system appropriately."
        ),
        query="transparency and information requirements for deployers",
    ),

    ComplianceRequirement(
        requirement_id="REQ-014",
        title="Human Oversight",
        description=(
            "The system should support effective human oversight."
        ),
        query="human oversight requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-015",
        title="Accuracy Robustness Cybersecurity",
        description=(
            "The system should provide appropriate levels of "
            "accuracy, robustness and cybersecurity."
        ),
        query="accuracy robustness cybersecurity requirements",
    ),
]