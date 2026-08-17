import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import PDFService
from app.services.system_profile_service import SystemProfileService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    temp_path = None

    try:
        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        result = PDFService.extract_text(temp_path)

        return {
            "filename": file.filename,
            "page_count": result["page_count"],
            "text": result["text"],
            "pages": result["pages"],
        }

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)


@router.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    temp_path = None

    try:

        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        document = PDFService.extract_text(temp_path)

        if not document["text"].strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF.",
            )

        profile_service = SystemProfileService()

        extraction = profile_service.extract_profile(
            pages=document["pages"]
        )

        return {
            "filename": file.filename,
            "page_count": document["page_count"],
            "system_profile": extraction.profile.model_dump(),
            "evidence": [
                item.model_dump()
                for item in extraction.evidence
            ],
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze PDF: {exc}",
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)