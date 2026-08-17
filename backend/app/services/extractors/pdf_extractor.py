from pathlib import Path

import pymupdf

from app.models.extracted_document import (
    DocumentSection,
    ExtractedDocument,
)


class PDFExtractor:

    @staticmethod
    def extract(
        file_path: str,
    ) -> ExtractedDocument:

        path = Path(file_path)

        document = pymupdf.open(path)

        sections: list[DocumentSection] = []

        try:
            for page_number, page in enumerate(
                document,
                start=1,
            ):
                text = page.get_text(
                    "text",
                    sort=True,
                )

                sections.append(
                    DocumentSection(
                        section_number=page_number,
                        text=text,
                    )
                )

            full_text = "\n\n".join(
                section.text
                for section in sections
            )

            return ExtractedDocument(
                filename=path.name,
                file_type="pdf",
                text=full_text,
                sections=sections,
                page_count=document.page_count,
            )

        finally:
            document.close()