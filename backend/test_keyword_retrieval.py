from app.db.database import SessionLocal
from app.services.retrieval_service import RetrievalService


db = SessionLocal()

try:
    retrieval = RetrievalService()

    results = retrieval.keyword_search(
    db=db,
    query="risk management system",        
    limit=5,
    )

    print(
        "Results found:",
        len(results),
    )

    for result in results:
        print("---------")
        print(result.article)
        print(result.text[:500])

finally:
    db.close()