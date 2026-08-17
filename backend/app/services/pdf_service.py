from pathlib import Path

import pymupdf


class PDFService:

    @staticmethod
    def extract_text(file_path: str) -> dict:

        path = Path(file_path)

        document = pymupdf.open(path)

        pages = []

        for page_number, page in enumerate(
            document,
            start=1,
        ):
            text = page.get_text(
                "text",
                sort=True,
            )

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

        full_text = "\n\n".join(
            page["text"]
            for page in pages
        )

        result = {
            "filename": path.name,
            "page_count": document.page_count,
            "text": full_text,
            "pages": pages,
        }

        document.close()

        return result