from openai import OpenAI

from app.config import settings


class LLMService:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=settings.groq_base_url,
        )

        self.model = settings.groq_model

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            response_format={
                "type": "json_object"
            },
            temperature=0,
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("LLM returned an empty response.")

        return content