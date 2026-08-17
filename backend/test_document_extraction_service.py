from app.services.document_extraction_service import (
    DocumentExtractionService,
)


service = DocumentExtractionService()


files = [
    "data/eu_ai_act.pdf",
    "data/test_system.txt",
    "data/test_system.md",
    "data/test_system.docx",
    "data/test_system01.docx",
]


for file_path in files:

    document = service.extract(
        file_path=file_path
    )

    print("\n" + "=" * 70)

    print("File:", document.filename)
    print("Type:", document.file_type)
    print("Sections:", len(document.sections))
    print("Pages:", document.page_count)
    print("Characters:", len(document.text))