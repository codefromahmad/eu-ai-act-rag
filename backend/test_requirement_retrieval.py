from app.db.database import SessionLocal
from app.services.requirement_registry import REQUIREMENTS
from app.services.requirement_retrieval_service import (
    RequirementRetrievalService,
)


db = SessionLocal()

try:
    service = RequirementRetrievalService()

    for requirement in REQUIREMENTS:

        print("\n" + "=" * 70)
        print(
            requirement.requirement_id,
            requirement.title,
        )
        print("=" * 70)

        references = service.retrieve_for_requirement(
            db=db,
            requirement=requirement,
            limit=3,
        )

        for reference in references:
            print(reference.article)

finally:
    db.close()