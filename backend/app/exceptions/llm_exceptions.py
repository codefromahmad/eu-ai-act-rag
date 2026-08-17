class LLMServiceError(Exception):
    """Base exception for LLM-related failures."""


class LLMRateLimitError(LLMServiceError):
    """Raised when the provider rate limit is exceeded."""


class LLMQuotaExceededError(LLMServiceError):
    """Raised when the provider daily quota is exhausted."""


class LLMResponseError(LLMServiceError):
    """Raised when the provider returns an invalid response."""