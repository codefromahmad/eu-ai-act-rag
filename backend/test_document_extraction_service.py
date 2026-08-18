from pathlib import Path

from app.services.document_extraction_service import (
    DocumentExtractionService,
)


service = DocumentExtractionService()


BACKEND_DIR = Path(__file__).resolve().parent
FIXTURES_DIR = BACKEND_DIR / "tests" / "fixtures"
DATA_DIR = BACKEND_DIR / "data"


files = [
    DATA_DIR / "eu_ai_act.pdf",
    FIXTURES_DIR / "test_system.txt",
    FIXTURES_DIR / "test_system.md",
    FIXTURES_DIR / "test_system.docx",
    FIXTURES_DIR / "test_system01.docx",
]


for file_path in files:

    document = service.extract(
        file_path=str(file_path)
    )

    print("\n" + "=" * 70)

    print("File:", document.filename)
    print("Type:", document.file_type)
    print("Sections:", len(document.sections))
    print("Pages:", document.page_count)
    print("Characters:", len(document.text))