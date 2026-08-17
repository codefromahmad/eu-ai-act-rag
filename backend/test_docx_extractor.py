from app.services.extractors.docx_extractor import (
    DOCXExtractor,
)


document = DOCXExtractor.extract(
    "data/test_system01.docx"
)


print("Filename:", document.filename)
print("Type:", document.file_type)
print("Sections:", len(document.sections))
print("Characters:", len(document.text))


print("\n--- SECTIONS ---")

for section in document.sections:

    print(
        f"\nSection {section.section_number}"
    )

    print(section.text[:1000])