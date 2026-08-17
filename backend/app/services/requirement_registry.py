from app.models.compliance import ComplianceRequirement


REQUIREMENTS = [
    ComplianceRequirement(
        requirement_id="REQ-009",
        title="Risk Management",
        description=(
            "The AI system should implement an appropriate "
            "risk management process."
        ),
        primary_article="Article 9",
        query="risk management system requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-010",
        title="Data and Data Governance",
        description=(
            "Training, validation and testing data should meet "
            "appropriate data governance and quality requirements."
        ),
        primary_article="Article 10",
        query="training validation testing data governance requirements",
    ),

    ComplianceRequirement(
        requirement_id="REQ-011",
        title="Technical Documentation",
        description=(
            "The system should have sufficient technical documentation."
        ),
        primary_article="Article 11",
        query="technical documentation requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-012",
        title="Record Keeping",
        description=(
            "The system should support appropriate logging "
            "and record keeping."
        ),
        primary_article="Article 12",
        query="automatic logging and record keeping requirements",
    ),

    ComplianceRequirement(
        requirement_id="REQ-013",
        title="Transparency",
        description=(
            "Deployers should receive sufficient information "
            "to understand and use the system appropriately."
        ),
        primary_article="Article 13",
        query="transparency and information requirements for deployers",
    ),

    ComplianceRequirement(
        requirement_id="REQ-014",
        title="Human Oversight",
        description=(
            "The system should support effective human oversight."
        ),
        primary_article="Article 14",
        query="human oversight requirements for high-risk AI systems",
    ),

    ComplianceRequirement(
        requirement_id="REQ-015",
        title="Accuracy Robustness Cybersecurity",
        description=(
            "The system should provide appropriate levels of "
            "accuracy, robustness and cybersecurity."
        ),
        primary_article="Article 15",
        query="accuracy robustness cybersecurity requirements",
    ),
]