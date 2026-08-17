from app.services.extractors.pdf_extractor import (
    PDFExtractor,
)


document = PDFExtractor.extract(
    "data/eu_ai_act.pdf"
)


print("Filename:", document.filename)
print("Type:", document.file_type)
print("Pages:", document.page_count)
print("Sections:", len(document.sections))
print("Characters:", len(document.text))

print("\n--- FIRST SECTION ---")
print(
    document.sections[0].text[:1000]
)