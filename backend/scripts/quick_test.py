from app.db.database import SessionLocal
from app.db.models.legal_chunk import LegalChunkDB

db = SessionLocal()

try:
    total = db.query(LegalChunkDB).count()

    with_embeddings = (
        db.query(LegalChunkDB)
        .filter(LegalChunkDB.embedding.isnot(None))
        .count()
    )

    print("Total chunks:", total)
    print("Chunks with embeddings:", with_embeddings)

finally:
    db.close()