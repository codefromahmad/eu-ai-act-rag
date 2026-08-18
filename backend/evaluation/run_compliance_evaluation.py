import argparse

from app.db.database import SessionLocal
from app.exceptions.llm_exceptions import (
    LLMQuotaExceededError,
)
from app.services.compliance_analysis_service import (
    ComplianceAnalysisService,
)
from app.services.requirement_registry import (
    REQUIREMENTS,
)
from evaluation.compliance_cases import (
    COMPLIANCE_CASES,
)
from evaluation.non_compliance_cases import (
    NON_COMPLIANCE_CASES,
)


ALL_COMPLIANCE_CASES = (
    COMPLIANCE_CASES
    + NON_COMPLIANCE_CASES
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

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="1-based index of first case to run.",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="1-based index of last case to run.",
    )

    args = parser.parse_args()

    start_index = max(
        args.start - 1,
        0,
    )

    end_index = (
        args.end
        if args.end is not None
        else len(ALL_COMPLIANCE_CASES)
    )

    selected_cases = (
        ALL_COMPLIANCE_CASES[
            start_index:end_index
        ]
    )

    db = SessionLocal()

    try:
        service = ComplianceAnalysisService()

        total = len(selected_cases)
        completed = 0
        passed = 0

        print(
            f"\nRunning {total} "
            "compliance evaluation cases...\n"
        )

        for case_number, case in enumerate(
            selected_cases,
            start=start_index + 1,
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

            try:

                if not relevant_evidence:

                    result = (
                        service
                        ._create_unknown_assessment(
                            requirement=requirement,
                            legal_references=legal_references,
                        )
                    )

                else:

                    result = (
                        service.assess_requirement(
                            profile=case["profile"],
                            user_evidence=relevant_evidence,
                            requirement=requirement,
                            legal_references=legal_references,
                        )
                    )

            except LLMQuotaExceededError:

                print("\n" + "=" * 70)

                print(
                    f"Stopped at case {case_number}: "
                    "LLM daily quota exhausted."
                )

                print(
                    "\nResume later with:"
                )

                print(
                    "python -m "
                    "evaluation.run_compliance_evaluation "
                    f"--start {case_number}"
                )

                break

            expected = case["expected"]

            success = (
                result.status == expected
            )

            completed += 1

            if success:
                passed += 1

            print("\n" + "=" * 70)

            print(
                f"Case {case_number}:",
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

        print("\n" + "=" * 70)

        print(
            "CURRENT COMPLIANCE EVALUATION RESULTS"
        )

        print("=" * 70)

        print(
            "Completed:",
            f"{completed}/{total}",
        )

        print(
            "Passed:",
            (
                f"{passed}/{completed}"
                if completed > 0
                else "0/0"
            ),
        )

        if completed > 0:

            accuracy = (
                passed
                / completed
                * 100
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