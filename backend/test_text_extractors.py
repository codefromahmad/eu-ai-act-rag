from app.services.extractors.markdown_extractor import (
    MarkdownExtractor,
)
from app.services.extractors.text_extractor import (
    TextExtractor,
)


txt_document = TextExtractor.extract(
    "data/test_system.txt"
)

md_document = MarkdownExtractor.extract(
    "data/test_system.md"
)


print("--- TXT ---")
print("Filename:", txt_document.filename)
print("Type:", txt_document.file_type)
print("Sections:", len(txt_document.sections))
print(txt_document.text)


print("\n--- MARKDOWN ---")
print("Filename:", md_document.filename)
print("Type:", md_document.file_type)
print("Sections:", len(md_document.sections))

for section in md_document.sections:
    print(
        f"\nSection {section.section_number}"
    )
    print(section.text)