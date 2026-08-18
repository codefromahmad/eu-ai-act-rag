import re

from app.services.pdf_service import PDFService


document = PDFService.extract_text(
    "data/eu_ai_act.pdf"
)

text = document["text"]


# Find every occurrence that looks like "Ar ticle 1"
pattern = re.compile(
    r"Ar\s+ticle\s+1\b",
    re.IGNORECASE,
)

matches = list(pattern.finditer(text))

print("Matches found:", len(matches))


for index, match in enumerate(matches, start=1):

    print(f"\n--- MATCH {index} ---")

    start = max(
        0,
        match.start() - 150
    )

    end = min(
        len(text),
        match.end() + 400
    )

    print(text[start:end])

    print("\n" + "=" * 70)