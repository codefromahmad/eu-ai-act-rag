from app.services.text_cleaning_service import TextCleaningService


sample = """
Ar ticle 9
Risk management sys tem

A r isk managem ent system shall be established.
The ar tif icial intelligence syste ms shall be monitored.
"""


cleaned = TextCleaningService.clean_legal_text(sample)

print("--- ORIGINAL ---")
print(sample)

print("\n--- CLEANED ---")
print(cleaned)