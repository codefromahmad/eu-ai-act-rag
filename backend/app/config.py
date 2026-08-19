from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EU AI Act RAG Compliance Analyzer"
    app_version: str = "0.1.0"

    debug: bool = False
    environment: str = "development"

    groq_api_key: str
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str

    database_url: str

    cors_origins: str = "http://localhost:5173"

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
        # Some cloud providers return postgres://
        # while SQLAlchemy expects postgresql://.
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