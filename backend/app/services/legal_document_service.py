from sqlalchemy.orm import Session

from app.repositories.legal_chunk_repository import (
    LegalChunkRepository,
)
from app.services.embedding_service import EmbeddingService
from app.services.legal_ingestion_service import (
    LegalIngestionService,
)
from app.services.pdf_service import PDFService


class LegalDocumentService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def ingest_pdf(
        self,
        db: Session,
        file_path: str,
        document_name: str,
        source: str | None = None,
        version: str | None = None,
    ):

        # 1. Extract PDF text
        document = PDFService.extract_text(
            file_path
        )

        # 2. Parse Articles
        article_chunks = (
            LegalIngestionService.split_articles(
                text=document["text"],
                document_name=document_name,
                source=source,
                version=version,
            )
        )

        # 3. Parse Annexes
        annex_chunks = (
            LegalIngestionService.split_annexes(
                text=document["text"],
                document_name=document_name,
                source=source,
                version=version,
            )
        )

        # 4. Combine both legal structures
        chunks = (
            article_chunks
            + annex_chunks
        )

        # 5. Generate embeddings
        embeddings = []

        for chunk in chunks:

            embedding = (
                self.embedding_service.embed_text(
                    chunk.text
                )
            )

            embeddings.append(
                embedding
            )

        # 6. Store everything in PostgreSQL
        LegalChunkRepository.save_many(
            db=db,
            chunks=chunks,
            embeddings=embeddings,
        )

        return chunks