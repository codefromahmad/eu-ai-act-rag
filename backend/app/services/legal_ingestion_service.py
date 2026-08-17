import re
import uuid

from app.models.legal_document import LegalChunk


class LegalIngestionService:

    ARTICLE_PATTERN = re.compile(
        r"^\s*Article\s+(\d+[a-zA-Z]?)\s*$",
        re.IGNORECASE | re.MULTILINE,
    )

    @classmethod
    def split_articles(
        cls,
        text: str,
        document_name: str,
        source: str | None = None,
        version: str | None = None,
    ) -> list[LegalChunk]:

        matches = list(
            cls.ARTICLE_PATTERN.finditer(text)
        )

        chunks: list[LegalChunk] = []

        for index, match in enumerate(matches):

            start = match.start()

            if index + 1 < len(matches):
                end = matches[index + 1].start()
            else:
                end = len(text)

            article_text = text[start:end].strip()

            article_number = match.group(1)

            chunks.append(
                LegalChunk(
                    chunk_id=str(uuid.uuid4()),
                    document=document_name,
                    article=f"Article {article_number}",
                    text=article_text,
                    source=source,
                    version=version,
                )
            )

        return chunks