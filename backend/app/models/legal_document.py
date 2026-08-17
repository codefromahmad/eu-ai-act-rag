from pydantic import BaseModel


class LegalChunk(BaseModel):
    chunk_id: str

    document: str

    article: str | None = None
    recital: str | None = None
    annex: str | None = None

    heading: str | None = None

    text: str

    source: str | None = None
    version: str | None = None