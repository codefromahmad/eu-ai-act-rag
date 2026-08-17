from app.db.database import SessionLocal
from app.services.retrieval_service import RetrievalService


queries = [
    "human oversight requirements",
    "training data quality and data governance",
    "technical documentation",
    "record keeping and logging",
    "accuracy robustness and cybersecurity",
    "transparency information for deployers",
]


db = SessionLocal()

try:
    retrieval = RetrievalService()

    for query in queries:

        print("\n")
        print("=" * 70)
        print("QUERY:", query)
        print("=" * 70)

        results = retrieval.hybrid_search(
            db=db,
            query=query,
            limit=3,
        )

        for rank, result in enumerate(
            results,
            start=1,
        ):
            print(
                f"{rank}. {result.article}"
            )

finally:
    db.close()