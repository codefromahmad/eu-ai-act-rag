from app.db.database import SessionLocal
from app.services.legal_document_service import LegalDocumentService


db = SessionLocal()

try:
    service = LegalDocumentService()

    chunks = service.ingest_pdf(
        db=db,
        file_path="data/eu_ai_act.pdf",
        document_name="EU AI Act",
        source="Official Journal of the European Union",
        version="Regulation (EU) 2024/1689",
    )

    print(f"Ingested {len(chunks)} legal chunks.")

finally:
    db.close()