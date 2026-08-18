from app.services.pdf_service import PDFService


document = PDFService.extract_text(
    "data/eu_ai_act.pdf"
)

text = document["text"]


# Search for several possible PDF extraction variants
search_terms = [
    "Article 1",
    "Ar ticle 1",
    "ARTICLE 1",
    "AR TICLE 1",
]


for term in search_terms:

    position = text.find(term)

    print(
        f"{term!r}:",
        position
    )

    if position != -1:

        print("\nContext:")

        print(
            text[
                max(0, position - 200):
                position + 500
            ]
        )

        print("\n" + "=" * 70 + "\n")