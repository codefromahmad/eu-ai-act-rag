from app.db.database import SessionLocal
from app.services.legal_ingestion_service import (
    LegalIngestionService,
)
from app.repositories.legal_chunk_repository import (
    LegalChunkRepository,
)


sample_text = """
Article 1

This Regulation lays down harmonised rules.

Article 2

This Regulation applies to providers and deployers.
"""


db = SessionLocal()

try:
    chunks = LegalIngestionService.split_articles(
        text=sample_text,
        document_name="EU AI Act",
        source="Official EU source",
        version="2026",
    )

    LegalChunkRepository.save_many(
        db=db,
        chunks=chunks,
    )

    print(f"Saved {len(chunks)} chunks.")

finally:
    db.close()