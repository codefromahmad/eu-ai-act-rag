from app.db.database import SessionLocal
from app.services.compliance_analysis_service import (
    ComplianceAnalysisService,
)
from app.services.requirement_registry import (
    REQUIREMENTS,
)
from evaluation.compliance_cases import (
    COMPLIANCE_CASES,
)


def get_requirement(
    requirement_id: str,
):

    for requirement in REQUIREMENTS:

        if (
            requirement.requirement_id
            == requirement_id
        ):
            return requirement

    raise ValueError(
        f"Requirement not found: {requirement_id}"
    )


def main():

    db = SessionLocal()

    try:
        service = ComplianceAnalysisService()

        passed = 0
        total = len(COMPLIANCE_CASES)

        print(
            f"\nRunning {total} "
            "compliance evaluation cases...\n"
        )

        for index, case in enumerate(
            COMPLIANCE_CASES,
            start=1,
        ):

            requirement = get_requirement(
                case["requirement_id"]
            )

            legal_references = (
                service
                .requirement_retrieval
                .retrieve_for_requirement(
                    db=db,
                    requirement=requirement,
                    limit=3,
                )
            )

            relevant_evidence = (
                service
                .evidence_selection
                .select_for_requirement(
                    requirement_id=(
                        requirement.requirement_id
                    ),
                    evidence=case["evidence"],
                )
            )

            # No relevant evidence means UNKNOWN
            # without calling the LLM.
            if not relevant_evidence:

                result = (
                    service
                    ._create_unknown_assessment(
                        requirement=requirement,
                        legal_references=legal_references,
                    )
                )

            else:

                result = service.assess_requirement(
                    profile=case["profile"],
                    user_evidence=relevant_evidence,
                    requirement=requirement,
                    legal_references=legal_references,
                )

            expected = case["expected"]

            success = (
                result.status == expected
            )

            if success:
                passed += 1

            print("=" * 70)

            print(
                f"Case {index}:",
                case["name"],
            )

            print(
                "Requirement:",
                requirement.requirement_id,
            )

            print(
                "Expected:",
                expected.value,
            )

            print(
                "Predicted:",
                result.status.value,
            )

            print(
                "Result:",
                "PASS" if success else "FAIL",
            )

            print(
                "Explanation:",
                result.explanation,
            )

        accuracy = (
            passed
            / total
            * 100
        )

        print("\n" + "=" * 70)
        print(
            "FINAL COMPLIANCE EVALUATION"
        )
        print("=" * 70)

        print(
            "Passed:",
            f"{passed}/{total}",
        )

        print(
            "Accuracy:",
            round(
                accuracy,
                2,
            ),
            "%",
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()