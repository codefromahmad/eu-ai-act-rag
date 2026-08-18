import argparse

from app.db.database import SessionLocal
from app.exceptions.llm_exceptions import (
    LLMQuotaExceededError,
)
from app.services.risk_classification_service import (
    RiskClassificationService,
)
from evaluation.risk_classification_cases import (
    RISK_CLASSIFICATION_CASES,
)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="1-based index of the first case to run.",
    )

    parser.add_argument(
        "--end",
        type=int,
        default=None,
        help="1-based index of the last case to run.",
    )

    args = parser.parse_args()

    start_index = max(
        args.start - 1,
        0,
    )

    end_index = (
        args.end
        if args.end is not None
        else len(RISK_CLASSIFICATION_CASES)
    )

    selected_cases = (
        RISK_CLASSIFICATION_CASES[
            start_index:end_index
        ]
    )

    db = SessionLocal()

    try:
        service = RiskClassificationService()

        total = len(selected_cases)
        passed = 0
        completed = 0

        print(
            f"\nRunning {total} "
            "risk classification cases...\n"
        )

        for offset, case in enumerate(
            selected_cases,
            start=start_index + 1,
        ):

            try:
                result = service.classify(
                    db=db,
                    profile=case["profile"],
                )

            except LLMQuotaExceededError:

                print("\n" + "=" * 70)
                print(
                    f"Stopped at case {offset}: "
                    "LLM daily quota exhausted."
                )

                print(
                    "Re-run later with:"
                )

                print(
                    "python -m "
                    "evaluation.run_risk_classification_evaluation "
                    f"--start {offset}"
                )

                break

            expected = case["expected"]
            predicted = result.category

            success = (
                predicted == expected
            )

            completed += 1

            if success:
                passed += 1

            print("=" * 70)
            print(
                f"Case {offset}"
            )

            print(
                "Name:",
                case["name"],
            )

            print(
                "Expected:",
                expected.value,
            )

            print(
                "Predicted:",
                predicted.value,
            )

            print(
                "Confidence:",
                result.confidence,
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
            "CURRENT RUN RESULTS"
        )
        print("=" * 70)

        print(
            "Completed:",
            f"{completed}/{total}",
        )

        print(
            "Passed:",
            f"{passed}/{completed}"
            if completed > 0
            else "0/0",
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