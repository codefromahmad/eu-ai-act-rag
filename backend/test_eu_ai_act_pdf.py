from app.services.pdf_service import PDFService


pdf_path = "data/eu_ai_act.pdf"

document = PDFService.extract_text(pdf_path)

print("Filename:", document["filename"])
print("Page count:", document["page_count"])
print("Total characters:", len(document["text"]))

print("\n--- FIRST PAGE PREVIEW ---")
print(document["pages"][0]["text"][:1500])