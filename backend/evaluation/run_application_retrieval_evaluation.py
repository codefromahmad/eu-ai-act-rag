from app.db.database import SessionLocal
from app.services.classification_retrieval_service import (
    ClassificationRetrievalService,
)
from app.services.requirement_registry import REQUIREMENTS
from app.services.requirement_retrieval_service import (
    RequirementRetrievalService,
)


def get_requirement(
    requirement_id: str,
):

    for requirement in REQUIREMENTS:
        if requirement.requirement_id == requirement_id:
            return requirement

    raise ValueError(
        f"Requirement not found: {requirement_id}"
    )


def evaluate_requirement_case(
    db,
    service,
    requirement_id: str,
    expected: list[str],
):

    requirement = get_requirement(
        requirement_id
    )

    references = service.retrieve_for_requirement(
        db=db,
        requirement=requirement,
        limit=5,
    )

    retrieved = [
        reference.article
        for reference in references
    ]

    success = all(
        item in retrieved
        for item in expected
    )

    print("\n" + "=" * 70)
    print("Requirement:", requirement_id)
    print("Expected:", expected)
    print("Retrieved:", retrieved)

    print(
        "Result:",
        "PASS" if success else "FAIL",
    )

    return success


def evaluate_classification_case(
    db,
    service,
    query: str,
    expected: list[str],
):

    references = service.retrieve(
        db=db,
        query=query,
        limit=5,
    )

    retrieved = [
        reference.article
        for reference in references
    ]

    success = all(
        item in retrieved
        for item in expected
    )

    print("\n" + "=" * 70)
    print("Classification query:", query)
    print("Expected:", expected)
    print("Retrieved:", retrieved)

    print(
        "Result:",
        "PASS" if success else "FAIL",
    )

    return success


def main():

    db = SessionLocal()

    try:
        requirement_service = (
            RequirementRetrievalService()
        )

        classification_service = (
            ClassificationRetrievalService()
        )

        results = []

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-009",
                expected=[
                    "Article 9"
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-010",
                expected=[
                    "Article 10"
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-011",
                expected=[
                    "Article 11",
                    "Annex IV",
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-012",
                expected=[
                    "Article 12"
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-013",
                expected=[
                    "Article 13"
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-014",
                expected=[
                    "Article 14"
                ],
            )
        )

        results.append(
            evaluate_requirement_case(
                db=db,
                service=requirement_service,
                requirement_id="REQ-015",
                expected=[
                    "Article 15"
                ],
            )
        )

        results.append(
            evaluate_classification_case(
                db=db,
                service=classification_service,
                query=(
                    "AI recruitment and "
                    "candidate selection"
                ),
                expected=[
                    "Article 6",
                    "Annex III",
                ],
            )
        )

        passed = sum(
            1
            for result in results
            if result
        )

        total = len(
            results
        )

        accuracy = (
            passed
            / total
            * 100
        )

        print("\n" + "=" * 70)
        print("FINAL APPLICATION RETRIEVAL RESULTS")
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