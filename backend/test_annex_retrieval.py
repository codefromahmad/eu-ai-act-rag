from app.db.database import SessionLocal
from app.services.retrieval_service import RetrievalService


db = SessionLocal()

try:
    retrieval = RetrievalService()

    results = retrieval.hybrid_search(
        db=db,
        query="AI systems used for recruitment and candidate selection",
        limit=5,
    )

    print("Results found:", len(results))

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print("\n" + "=" * 70)
        print(f"Rank: {rank}")

        if result.article:
            print("Article:", result.article)

        if result.annex:
            print("Annex:", result.annex)

        print(result.text[:800])

finally:
    db.close()