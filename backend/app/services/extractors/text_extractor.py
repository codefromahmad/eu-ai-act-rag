from pathlib import Path

from app.models.extracted_document import (
    DocumentSection,
    ExtractedDocument,
)


class TextExtractor:

    @staticmethod
    def extract(
        file_path: str,
    ) -> ExtractedDocument:

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8"
        )

        return ExtractedDocument(
            filename=path.name,
            file_type="txt",
            text=text,
            sections=[
                DocumentSection(
                    section_number=1,
                    text=text,
                )
            ],
            page_count=None,
        )