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


# Look for headings such as:
# ANNEX I
# ANNEX II
# ANNEX III
pattern = re.compile(
    r"^\s*ANNEX\s+([IVXLCDM]+)\s*$",
    re.MULTILINE,
)


matches = list(
    pattern.finditer(text)
)


print(
    "Total annex headings detected:",
    len(matches),
)

print(
    "\n--- DETECTED ANNEXES ---"
)

for match in matches:
    print(
        f"ANNEX {match.group(1)}"
    )


# Show Annex III because it is important
# for high-risk classification.
annex_iii = next(
    (
        match
        for match in matches
        if match.group(1) == "III"
    ),
    None,
)


if annex_iii:

    print(
        "\n--- ANNEX III PREVIEW ---"
    )

    print(
        text[
            annex_iii.start():
            annex_iii.start() + 2500
        ]
    )

else:
    print(
        "\nANNEX III heading not found."
    )


document.close()