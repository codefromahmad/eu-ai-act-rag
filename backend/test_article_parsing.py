from app.services.pdf_service import PDFService
from app.services.legal_ingestion_service import LegalIngestionService


# 1. Read the EU AI Act PDF
document = PDFService.extract_text(
    "data/eu_ai_act.pdf"
)

# 2. Split it into article-based chunks
chunks = LegalIngestionService.split_articles(
    text=document["text"],
    document_name="EU AI Act",
    source="Official Journal of the European Union",
    version="Regulation (EU) 2024/1689",
)


# 3. Show basic results
print("Total articles detected:", len(chunks))

print("\n--- FIRST 10 DETECTED ARTICLES ---")

for chunk in chunks[:10]:
    print(
        chunk.article,
        "| characters:",
        len(chunk.text),
    )


print("\n--- FIRST ARTICLE PREVIEW ---")

if chunks:
    print(chunks[0].text[:1000])