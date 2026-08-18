from app.db.database import SessionLocal
from app.services.classification_retrieval_service import (
    ClassificationRetrievalService,
)


QUERIES = [
    "AI recruitment and candidate selection",
    "AI system used for hiring employees",
    "AI used to evaluate job applicants",
    "AI system used in education admissions",
    "AI system used for creditworthiness assessment",
]


def main():

    db = SessionLocal()

    try:
        service = ClassificationRetrievalService()

        passed = 0

        for query in QUERIES:

            references = service.retrieve(
                db=db,
                query=query,
                limit=5,
            )

            retrieved = [
                reference.article
                for reference in references
            ]

            has_article_6 = (
                "Article 6" in retrieved
            )

            has_annex_iii = (
                "Annex III" in retrieved
            )

            success = (
                has_article_6
                and has_annex_iii
            )

            if success:
                passed += 1

            print("\n" + "=" * 70)

            print("Query:")
            print(query)

            print("Retrieved:")
            print(retrieved)

            print(
                "Article 6 + Annex III:",
                "PASS" if success else "FAIL",
            )

        print("\n" + "=" * 70)

        score = (
            passed
            / len(QUERIES)
            * 100
        )

        print(
            "Classification retrieval accuracy:",
            round(score, 2),
            "%",
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()