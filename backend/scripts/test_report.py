from app.models.analysis_result import (
    AnalysisScore,
    FullComplianceAnalysis,
)
from app.models.compliance import (
    ComplianceAssessment,
    ComplianceStatus,
    LegalReference,
)
from app.models.risk_classification import (
    RiskCategory,
    RiskClassification,
)
from app.models.system_profile import (
    HumanOversight,
    SystemProfile,
)
from app.services.report_service import (
    ReportService,
)


# --------------------------------------------------
# 1. Mock system profile
# --------------------------------------------------

profile = SystemProfile(
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
            "before final decisions."
        ),
    ),
)


# --------------------------------------------------
# 2. Mock risk classification
# --------------------------------------------------

risk_classification = RiskClassification(
    category=RiskCategory.high_risk,
    ai_act_applicable=True,
    explanation=(
        "The system is used for recruitment and "
        "candidate ranking and appears to fall under "
        "the high-risk employment category."
    ),
    relevant_articles=[
        "Article 6"
    ],
    relevant_annexes=[
        "Annex III"
    ],
    indicators=[
        "Employment context",
        "Candidate ranking",
    ],
    missing_information=[],
    confidence=0.9,
)


# --------------------------------------------------
# 3. Mock compliance assessments
# --------------------------------------------------

assessments = [
    ComplianceAssessment(
        requirement_id="REQ-009",
        status=ComplianceStatus.unknown,
        explanation=(
            "No sufficient evidence about a documented "
            "risk management system was provided."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 9",
                text="Risk management requirements.",
            )
        ],
        recommendations=[
            "Document a continuous risk management process."
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-010",
        status=ComplianceStatus.unknown,
        explanation=(
            "No sufficient evidence about training data "
            "governance or data quality was provided."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 10",
                text="Data and data governance requirements.",
            )
        ],
        recommendations=[
            "Document data governance and quality controls."
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-011",
        status=ComplianceStatus.unknown,
        explanation=(
            "Technical documentation was not sufficiently "
            "described."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 11",
                text="Technical documentation requirements.",
            ),
            LegalReference(
                article="Annex IV",
                text="Technical documentation contents.",
            ),
        ],
        recommendations=[
            "Prepare technical documentation covering Annex IV."
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-012",
        status=ComplianceStatus.unknown,
        explanation=(
            "Logging and record-keeping capabilities "
            "were not described."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 12",
                text="Record-keeping requirements.",
            )
        ],
        recommendations=[
            "Implement automatic event logging."
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-013",
        status=ComplianceStatus.unknown,
        explanation=(
            "Transparency information for deployers "
            "was not sufficiently described."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 13",
                text="Transparency requirements.",
            )
        ],
        recommendations=[
            "Provide clear instructions for deployers."
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-014",
        status=ComplianceStatus.partial,
        explanation=(
            "Human oversight exists because HR reviews "
            "recommendations, but additional oversight "
            "controls are not documented."
        ),
        user_evidence=[
            (
                "HR staff review recommendations "
                "before final decisions."
            )
        ],
        legal_references=[
            LegalReference(
                article="Article 14",
                text="Human oversight requirements.",
            )
        ],
        recommendations=[
            "Document override and intervention procedures.",
            "Train HR staff on automation bias.",
        ],
    ),

    ComplianceAssessment(
        requirement_id="REQ-015",
        status=ComplianceStatus.unknown,
        explanation=(
            "Accuracy, robustness and cybersecurity "
            "measures were not described."
        ),
        user_evidence=[],
        legal_references=[
            LegalReference(
                article="Article 15",
                text=(
                    "Accuracy, robustness and "
                    "cybersecurity requirements."
                ),
            )
        ],
        recommendations=[
            "Document accuracy metrics and security controls."
        ],
    ),
]


# --------------------------------------------------
# 4. Deterministic score from previous test
# --------------------------------------------------

score = AnalysisScore(
    compliance_score=50.0,
    coverage=14.29,
    total_requirements=7,
    known_requirements=1,
    compliant=0,
    partial=1,
    non_compliant=0,
    unknown=6,
)


# --------------------------------------------------
# 5. Build analysis object
# --------------------------------------------------

analysis = FullComplianceAnalysis(
    risk_classification=risk_classification,
    assessments=assessments,
    score=score,
)


# --------------------------------------------------
# 6. Test only ReportService
# --------------------------------------------------

report_service = ReportService()

report = report_service.generate_report(
    profile=profile,
    analysis=analysis,
)


print(
    report.model_dump_json(
        indent=2
    )
)