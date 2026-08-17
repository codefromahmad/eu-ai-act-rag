from app.models.extracted_document import (
    DocumentSection,
    ExtractedDocument,
)


document = ExtractedDocument(
    filename="system_description.txt",
    file_type="txt",
    text="This system ranks candidates.",
    sections=[
        DocumentSection(
            section_number=1,
            text="This system ranks candidates.",
        )
    ],
)


print(
    document.model_dump_json(
        indent=2
    )
)