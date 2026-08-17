import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.db.database import SessionLocal
from app.exceptions.llm_exceptions import (
    LLMQuotaExceededError,
    LLMRateLimitError,
    LLMResponseError,
    LLMServiceError,
)
from app.services.compliance_pipeline_service import (
    CompliancePipelineService,
)
from app.services.pdf_service import PDFService
from app.services.system_profile_service import (
    SystemProfileService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def validate_pdf(file: UploadFile) -> None:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


def handle_llm_exception(exc: Exception) -> None:

    if isinstance(exc, LLMQuotaExceededError):
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service has temporarily exhausted "
                "its usage quota. Please try again later."
            ),
        )

    if isinstance(exc, LLMRateLimitError):
        raise HTTPException(
            status_code=429,
            detail=(
                "The AI service is receiving too many requests. "
                "Please try again shortly."
            ),
        )

    if isinstance(exc, LLMResponseError):
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service returned an invalid response."
            ),
        )

    if isinstance(exc, LLMServiceError):
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service is temporarily unavailable."
            ),
        )


@router.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...)
):

    validate_pdf(file)

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

        result = PDFService.extract_text(
            temp_path
        )

        if not result["text"].strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF.",
            )

        return {
            "filename": file.filename,
            "page_count": result["page_count"],
            "text": result["text"],
            "pages": result["pages"],
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to extract the PDF.",
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(
                missing_ok=True
            )


@router.post("/analyze")
async def analyze_pdf(
    file: UploadFile = File(...)
):

    validate_pdf(file)

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

        document = PDFService.extract_text(
            temp_path
        )

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
            "system_profile": (
                extraction.profile.model_dump()
            ),
            "evidence": [
                item.model_dump()
                for item in extraction.evidence
            ],
        }

    except HTTPException:
        raise

    except (
        LLMQuotaExceededError,
        LLMRateLimitError,
        LLMResponseError,
        LLMServiceError,
    ) as exc:
        handle_llm_exception(exc)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while analyzing the PDF."
            ),
        )

    finally:
        if temp_path:
            Path(temp_path).unlink(
                missing_ok=True
            )


@router.post("/report")
async def generate_compliance_report(
    file: UploadFile = File(...)
):

    validate_pdf(file)

    temp_path = None
    db = None

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

        db = SessionLocal()

        pipeline = CompliancePipelineService()

        result = pipeline.analyze_pdf(
            db=db,
            file_path=temp_path,
        )

        return {
            "filename": file.filename,
            "page_count": result["page_count"],
            "system_profile": (
                result["system_profile"].model_dump()
            ),
            "user_evidence": [
                evidence.model_dump()
                for evidence
                in result["user_evidence"]
            ],
            "report": (
                result["report"].model_dump()
            ),
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except (
        LLMQuotaExceededError,
        LLMRateLimitError,
        LLMResponseError,
        LLMServiceError,
    ) as exc:
        handle_llm_exception(exc)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred while "
                "generating the compliance report."
            ),
        )

    finally:
        if db:
            db.close()

        if temp_path:
            Path(temp_path).unlink(
                missing_ok=True
            )