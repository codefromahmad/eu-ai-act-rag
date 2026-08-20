import time

from openai import (
    APIError,
    APITimeoutError,
    APIStatusError,
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
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
            timeout=60.0,
            max_retries=0,
        )

        self.model = settings.llm_model

    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        max_retries: int = 3,
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
                if attempt == max_retries:
                    raise LLMRateLimitError(
                        "The LLM provider rate limit "
                        "was exceeded after multiple retries."
                    ) from exc

                wait_seconds = 2 * attempt

                print(
                    "LLM rate limit reached. "
                    f"Waiting {wait_seconds} seconds "
                    f"before retry {attempt}/{max_retries}..."
                )

                time.sleep(wait_seconds)

            except APITimeoutError as exc:
                if attempt == max_retries:
                    raise LLMServiceError(
                        "The LLM request timed out."
                    ) from exc

                wait_seconds = 2 * attempt

                print(
                    "LLM request timed out. "
                    f"Waiting {wait_seconds} seconds "
                    f"before retry {attempt}/{max_retries}..."
                )

                time.sleep(wait_seconds)

            except APIStatusError as exc:
                status_code = exc.status_code

                if status_code == 402:
                    raise LLMQuotaExceededError(
                        "The LLM account has insufficient credits."
                    ) from exc

                if status_code == 429:
                    raise LLMRateLimitError(
                        "The LLM provider rate limit was exceeded."
                    ) from exc

                if status_code in (
                    502,
                    503,
                    524,
                    529,
                ):
                    raise LLMServiceError(
                        "The selected LLM provider "
                        "is temporarily unavailable."
                    ) from exc

                raise LLMServiceError(
                    "The LLM provider returned "
                    f"HTTP {status_code}."
                ) from exc

            except APIError as exc:
                raise LLMServiceError(
                    "The LLM provider returned an API error."
                ) from exc

        raise LLMServiceError(
            "LLM request failed after maximum retries."
        )