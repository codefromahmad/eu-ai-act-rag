import re

import pymupdf


pdf_path = "data/eu_ai_act.pdf"

document = pymupdf.open(pdf_path)

full_text = []

for page in document:
    text = page.get_text(
        "text",
        sort=True,
    )
    full_text.append(text)

text = "\n".join(full_text)


# Article must appear alone on a line.
pattern = re.compile(
    r"^\s*Article\s+(\d+[A-Za-z]?)\s*$",
    re.MULTILINE,
)

matches = list(pattern.finditer(text))


print("Total article headings detected:", len(matches))

print("\n--- FIRST 10 ARTICLES ---")

for match in matches[:10]:
    print(
        f"Article {match.group(1)}"
    )


# Find the real Article 9 heading
article_9 = next(
    (
        match
        for match in matches
        if match.group(1) == "9"
    ),
    None,
)


if article_9:

    print("\n--- ACTUAL ARTICLE 9 PREVIEW ---")

    print(
        text[
            article_9.start():
            article_9.start() + 1500
        ]
    )

else:
    print("\nArticle 9 heading not found.")