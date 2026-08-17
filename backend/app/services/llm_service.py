import time

from openai import OpenAI, RateLimitError

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
        max_retries: int = 5,
    ) -> str:

        for attempt in range(1, max_retries + 1):

            try:
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

                content = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if not content:
                    raise ValueError(
                        "LLM returned an empty response."
                    )

                return content

            except RateLimitError as exc:

                if attempt == max_retries:
                    raise

                wait_seconds = 3 * attempt

                print(
                    f"Groq rate limit reached. "
                    f"Waiting {wait_seconds} seconds "
                    f"before retry {attempt}/{max_retries}..."
                )

                time.sleep(wait_seconds)

        raise RuntimeError(
            "LLM request failed after maximum retries."
        )