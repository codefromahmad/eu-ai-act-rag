from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EU AI Act RAG Compliance Analyzer"
    app_version: str = "0.1.0"

    debug: bool = False
    environment: str = "development"

    # LLM configuration
    llm_api_key: str
    llm_base_url: str
    llm_model: str

    # Database
    database_url: str

    # CORS
    cors_origins: str = "http://localhost:5173"

    # Embeddings
    embedding_backend: str = "torch"

    @property
    def allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]

    @field_validator(
        "database_url",
        mode="before",
    )
    @classmethod
    def normalize_database_url(
        cls,
        value: str,
    ) -> str:
        if value.startswith("postgres://"):
            return value.replace(
                "postgres://",
                "postgresql://",
                1,
            )

        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()