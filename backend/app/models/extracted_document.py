from pydantic import BaseModel, Field


class DocumentSection(BaseModel):
    section_number: int
    text: str


class ExtractedDocument(BaseModel):
    filename: str
    file_type: str
    text: str

    sections: list[DocumentSection] = Field(
        default_factory=list
    )

    page_count: int | None = None