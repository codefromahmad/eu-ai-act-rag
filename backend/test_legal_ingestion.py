from app.services.legal_ingestion_service import (
    LegalIngestionService,
)


sample_text = """
Article 1

This Regulation lays down harmonised rules...

Article 2

This Regulation applies to...

Article 3

For the purposes of this Regulation...
"""


chunks = LegalIngestionService.split_articles(
    text=sample_text,
    document_name="EU AI Act",
    source="Official EU source",
    version="2026",
)


for chunk in chunks:
    print("-----------")
    print(chunk.article)
    print(chunk.text)