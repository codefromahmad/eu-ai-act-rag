from pathlib import Path

from app.models.extracted_document import ExtractedDocument
from app.services.extractors.docx_extractor import DOCXExtractor
from app.services.extractors.markdown_extractor import MarkdownExtractor
from app.services.extractors.pdf_extractor import PDFExtractor
from app.services.extractors.text_extractor import TextExtractor


class DocumentExtractionService:

    SUPPORTED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
    }

    def extract(
        self,
        file_path: str,
    ) -> ExtractedDocument:

        path = Path(file_path)

        extension = path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":
            return PDFExtractor.extract(
                file_path
            )

        if extension == ".docx":
            return DOCXExtractor.extract(
                file_path
            )

        if extension == ".txt":
            return TextExtractor.extract(
                file_path
            )

        if extension == ".md":
            return MarkdownExtractor.extract(
                file_path
            )

        raise ValueError(
            "No extractor available for this file type."
        )