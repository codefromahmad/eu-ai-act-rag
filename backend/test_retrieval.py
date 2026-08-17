from app.db.database import SessionLocal
from app.services.retrieval_service import (
    RetrievalService,
)


db = SessionLocal()

try:

    retrieval = RetrievalService()

    results = retrieval.semantic_search(
        db=db,
        query="risk management requirements",
        limit=3,
    )

    for result in results:
        print("---------")
        print(result.article)
        print(result.text[:500])

finally:
    db.close()