import json

from app.models.evidence import SystemProfileExtraction
from app.services.llm_service import LLMService


class SystemProfileService:

    def __init__(self):
        self.llm = LLMService()

    def extract_profile(
        self,
        pages: list[dict],
    ) -> SystemProfileExtraction:

        system_prompt = """
You are an AI system information extraction assistant.

Extract factual information about the AI system described
in the provided document.

Do NOT perform EU AI Act compliance analysis.

Rules:

1. Only use information explicitly supported by the document.
2. Never invent missing information.
3. Use null for unknown scalar fields.
4. Use [] for unknown list fields.
5. Add important missing information to unknown_information.
6. Keep descriptions concise.
7. Every important extracted fact should have evidence.
8. Evidence must contain the page number where it was found.
9. The quote must come from the provided document.
10. Return only valid JSON.
"""

        document = "\n\n".join(
            f"""
--- PAGE {page["page_number"]} ---
{page["text"]}
"""
            for page in pages
        )

        schema = SystemProfileExtraction.model_json_schema()

        user_prompt = f"""
Extract a structured AI system profile from this document.

Return JSON matching exactly this schema:

{json.dumps(schema, indent=2)}

For evidence:

field:
The SystemProfile field being supported.

value:
The extracted value.

page_number:
The PDF page containing the evidence.

quote:
A short exact passage supporting the extracted information.

DOCUMENT:

{document}
"""

        raw_response = self.llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        data = json.loads(raw_response)

        return SystemProfileExtraction.model_validate(data)