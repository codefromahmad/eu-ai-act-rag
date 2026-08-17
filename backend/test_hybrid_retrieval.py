from app.db.database import SessionLocal
from app.services.retrieval_service import RetrievalService


db = SessionLocal()

try:
    retrieval = RetrievalService()

    results = retrieval.hybrid_search(
        db=db,
        query="risk management system",
        limit=5,
    )

    print("Results found:", len(results))

    for rank, result in enumerate(
        results,
        start=1,
    ):
        print("---------")
        print(f"Rank: {rank}")
        print(result.article)
        print(result.text[:400])

finally:
    db.close()