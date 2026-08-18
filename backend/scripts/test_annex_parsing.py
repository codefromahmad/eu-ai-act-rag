from app.services.legal_ingestion_service import (
    LegalIngestionService,
)
from app.services.pdf_service import PDFService


document = PDFService.extract_text(
    "data/eu_ai_act.pdf"
)


annexes = LegalIngestionService.split_annexes(
    text=document["text"],
    document_name="EU AI Act",
    source="Official Journal of the European Union",
    version="Regulation (EU) 2024/1689",
)


print(
    "Total annexes detected:",
    len(annexes),
)


print(
    "\n--- DETECTED ANNEXES ---"
)

for annex in annexes:
    print(
        annex.annex,
        "| characters:",
        len(annex.text),
    )


annex_iii = next(
    (
        annex
        for annex in annexes
        if annex.annex == "Annex III"
    ),
    None,
)


if annex_iii:

    print(
        "\n--- ANNEX III PREVIEW ---"
    )

    print(
        annex_iii.text[:2000]
    )