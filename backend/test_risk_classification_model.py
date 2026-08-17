from app.models.risk_classification import (
    RiskCategory,
    RiskClassification,
)


classification = RiskClassification(
    category=RiskCategory.high_risk,
    ai_act_applicable=True,
    explanation=(
        "The AI system is used in an employment context "
        "for candidate ranking."
    ),
    relevant_articles=[
        "Article 6"
    ],
    relevant_annexes=[
        "Annex III"
    ],
    indicators=[
        "Employment domain",
        "Candidate ranking",
        "Used by HR staff",
    ],
    missing_information=[],
    confidence=0.95,
)


print(
    classification.model_dump_json(
        indent=2
    )
)