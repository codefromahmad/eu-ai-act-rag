from pathlib import Path

from app.models.extracted_document import (
    DocumentSection,
    ExtractedDocument,
)


class MarkdownExtractor:

    @staticmethod
    def extract(
        file_path: str,
    ) -> ExtractedDocument:

        path = Path(file_path)

        text = path.read_text(
            encoding="utf-8"
        )

        sections: list[DocumentSection] = []

        current_lines: list[str] = []
        section_number = 1

        for line in text.splitlines():

            if (
                line.startswith("#")
                and current_lines
            ):
                sections.append(
                    DocumentSection(
                        section_number=section_number,
                        text="\n".join(
                            current_lines
                        ).strip(),
                    )
                )

                section_number += 1
                current_lines = []

            current_lines.append(line)

        if current_lines:
            sections.append(
                DocumentSection(
                    section_number=section_number,
                    text="\n".join(
                        current_lines
                    ).strip(),
                )
            )

        return ExtractedDocument(
            filename=path.name,
            file_type="md",
            text=text,
            sections=sections,
            page_count=None,
        )