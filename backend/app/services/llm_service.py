import time

from openai import (
    APIError,
    OpenAI,
    RateLimitError,
)

from app.config import settings
from app.exceptions.llm_exceptions import (
    LLMQuotaExceededError,
    LLMRateLimitError,
    LLMResponseError,
    LLMServiceError,
)


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

        for attempt in range(
            1,
            max_retries + 1,
        ):

            try:
                response = (
                    self.client
                    .chat
                    .completions
                    .create(
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
                )

                content = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                if not content:
                    raise LLMResponseError(
                        "LLM returned an empty response."
                    )

                return content

            except RateLimitError as exc:

                message = str(exc).lower()

                # Daily quota / tokens-per-day exhausted.
                # Waiting a few seconds will not solve this.
                if (
                    "tokens per day" in message
                    or "tpd" in message
                ):
                    raise LLMQuotaExceededError(
                        "The LLM provider daily quota "
                        "has been exhausted."
                    ) from exc

                # Short-term rate limit.
                if attempt == max_retries:
                    raise LLMRateLimitError(
                        "The LLM provider rate limit "
                        "was exceeded after multiple retries."
                    ) from exc

                wait_seconds = 3 * attempt

                print(
                    "Groq rate limit reached. "
                    f"Waiting {wait_seconds} seconds "
                    f"before retry {attempt}/{max_retries}..."
                )

                time.sleep(
                    wait_seconds
                )

            except APIError as exc:
                raise LLMServiceError(
                    "The LLM provider returned an API error."
                ) from exc

        raise LLMServiceError(
            "LLM request failed after maximum retries."
        )