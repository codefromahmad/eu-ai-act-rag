from app.db.database import SessionLocal
from app.services.retrieval_service import RetrievalService
from evaluation.retrieval_cases import RETRIEVAL_CASES


TOP_K = 5


def get_reference_name(result) -> str | None:

    if result.article:
        return result.article

    if result.annex:
        return result.annex

    return None


def contains_any(
    expected: list[str],
    retrieved: list[str],
) -> bool:

    return any(
        item in retrieved
        for item in expected
    )


def contains_all(
    expected: list[str],
    retrieved: list[str],
) -> bool:

    return all(
        item in retrieved
        for item in expected
    )


def main():

    db = SessionLocal()

    try:
        retrieval = RetrievalService()

        total_cases = len(
            RETRIEVAL_CASES
        )

        any_hit_at_1 = 0
        any_hit_at_3 = 0
        any_hit_at_5 = 0

        all_expected_at_1 = 0
        all_expected_at_3 = 0
        all_expected_at_5 = 0

        print(
            f"\nRunning {total_cases} "
            "retrieval evaluation cases...\n"
        )

        for index, case in enumerate(
            RETRIEVAL_CASES,
            start=1,
        ):

            results = retrieval.hybrid_search(
                db=db,
                query=case["query"],
                limit=TOP_K,
            )

            retrieved = [
                get_reference_name(
                    result
                )
                for result in results
            ]

            retrieved = [
                reference
                for reference in retrieved
                if reference
            ]

            expected = case["expected"]

            retrieved_at_1 = retrieved[:1]
            retrieved_at_3 = retrieved[:3]
            retrieved_at_5 = retrieved[:5]

            any1 = contains_any(
                expected,
                retrieved_at_1,
            )

            any3 = contains_any(
                expected,
                retrieved_at_3,
            )

            any5 = contains_any(
                expected,
                retrieved_at_5,
            )

            all1 = contains_all(
                expected,
                retrieved_at_1,
            )

            all3 = contains_all(
                expected,
                retrieved_at_3,
            )

            all5 = contains_all(
                expected,
                retrieved_at_5,
            )

            if any1:
                any_hit_at_1 += 1

            if any3:
                any_hit_at_3 += 1

            if any5:
                any_hit_at_5 += 1

            if all1:
                all_expected_at_1 += 1

            if all3:
                all_expected_at_3 += 1

            if all5:
                all_expected_at_5 += 1

            print("=" * 70)
            print(f"Case {index}")

            print(
                "Query:",
                case["query"],
            )

            print(
                "Expected:",
                expected,
            )

            print(
                "Retrieved:",
                retrieved,
            )

            print(
                "Any Hit@1:",
                "PASS" if any1 else "FAIL",
            )

            print(
                "Any Hit@3:",
                "PASS" if any3 else "FAIL",
            )

            print(
                "Any Hit@5:",
                "PASS" if any5 else "FAIL",
            )

            print(
                "All Expected@1:",
                "PASS" if all1 else "FAIL",
            )

            print(
                "All Expected@3:",
                "PASS" if all3 else "FAIL",
            )

            print(
                "All Expected@5:",
                "PASS" if all5 else "FAIL",
            )

        print("\n" + "=" * 70)
        print("FINAL RESULTS")
        print("=" * 70)

        def percentage(
            value: int,
        ) -> float:

            return round(
                value
                / total_cases
                * 100,
                2,
            )

        print(
            "Any Hit@1:",
            percentage(
                any_hit_at_1
            ),
            "%",
        )

        print(
            "Any Hit@3:",
            percentage(
                any_hit_at_3
            ),
            "%",
        )

        print(
            "Any Hit@5:",
            percentage(
                any_hit_at_5
            ),
            "%",
        )

        print(
            "All Expected@1:",
            percentage(
                all_expected_at_1
            ),
            "%",
        )

        print(
            "All Expected@3:",
            percentage(
                all_expected_at_3
            ),
            "%",
        )

        print(
            "All Expected@5:",
            percentage(
                all_expected_at_5
            ),
            "%",
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()