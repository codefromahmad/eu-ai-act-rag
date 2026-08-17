import re


class TextCleaningService:

    @staticmethod
    def clean_legal_text(text: str) -> str:

        # Fix spaces inside broken words:
        # "r isk" -> "risk"
        # "managem ent" -> "management"
        # "Ar ticle" -> "Article"
        text = re.sub(
            r"\b([A-Za-z]{1,4})\s+([a-z]{2,})\b",
            r"\1\2",
            text,
        )

        # Remove repeated spaces
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        # Normalize excessive blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()