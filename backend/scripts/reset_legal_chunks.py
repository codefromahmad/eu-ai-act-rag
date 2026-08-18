from app.db.database import SessionLocal
from app.db.models.legal_chunk import LegalChunkDB


db = SessionLocal()

try:
    deleted = db.query(LegalChunkDB).delete()

    db.commit()

    print(f"Deleted {deleted} legal chunks.")

finally:
    db.close()