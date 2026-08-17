from pathlib import Path

from app.services.document_extraction_service import (
    DocumentExtractionService,
)


def test_extract_txt_document():

    service = DocumentExtractionService()

    document = service.extract(
        "data/test_system.txt"
    )

    assert document.file_type == "txt"
    assert document.filename == "test_system.txt"
    assert len(document.sections) == 1
    assert document.page_count is None
    assert "ranks job candidates" in document.text


def test_extract_markdown_document():

    service = DocumentExtractionService()

    document = service.extract(
        "data/test_system.md"
    )

    assert document.file_type == "md"
    assert len(document.sections) == 3
    assert document.page_count is None


def test_extract_docx_document():

    service = DocumentExtractionService()

    document = service.extract(
        "data/test_system01.docx"
    )

    assert document.file_type == "docx"
    assert len(document.sections) == 3
    assert document.page_count is None


def test_unsupported_document_is_rejected(tmp_path):

    file_path = tmp_path / "test.jpg"

    file_path.write_bytes(
        b"fake image content"
    )

    service = DocumentExtractionService()

    try:
        service.extract(
            str(file_path)
        )

        assert False, (
            "Expected unsupported file type error."
        )

    except ValueError as exc:
        assert "Unsupported file type" in str(exc)