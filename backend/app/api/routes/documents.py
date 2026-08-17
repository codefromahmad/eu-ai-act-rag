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
from app.services.full_analysis_service import FullAnalysisService
from app.services.pdf_service import PDFService
from app.services.report_service import ReportService
from app.services.system_profile_service import SystemProfileService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def validate_pdf(file: UploadFile) -> None:
    """
    Validate that the uploaded file is a PDF.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )


def handle_llm_exception(exc: Exception) -> None:
    """
    Convert internal LLM exceptions into clean API responses.
    """

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
    """
    Extract raw text and page-level content from a PDF.
    """

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
                detail=(
                    "No readable text was found "
                    "in the PDF."
                ),
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
    """
    Extract a structured AI-system profile and evidence
    from an uploaded PDF.
    """

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
                detail=(
                    "No readable text was found "
                    "in the PDF."
                ),
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
    """
    Run the complete EU AI Act analysis pipeline.

    PDF
    → SystemProfile
    → Evidence
    → Risk classification
    → Requirement assessment
    → Scoring
    → Final report
    """

    validate_pdf(file)

    temp_path = None
    db = None

    try:
        # ----------------------------------------------
        # 1. Save uploaded PDF temporarily
        # ----------------------------------------------

        with NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file,
            )

            temp_path = temp_file.name

        # ----------------------------------------------
        # 2. Extract PDF text
        # ----------------------------------------------

        document = PDFService.extract_text(
            temp_path
        )

        if not document["text"].strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the PDF."
                ),
            )

        # ----------------------------------------------
        # 3. Extract SystemProfile + evidence
        # ----------------------------------------------

        profile_service = SystemProfileService()

        extraction = profile_service.extract_profile(
            pages=document["pages"]
        )

        # ----------------------------------------------
        # 4. Open database
        # ----------------------------------------------

        db = SessionLocal()

        # ----------------------------------------------
        # 5. Run risk-aware compliance analysis
        # ----------------------------------------------

        full_analysis_service = FullAnalysisService()

        analysis = full_analysis_service.analyze(
            db=db,
            profile=extraction.profile,
            user_evidence=extraction.evidence,
        )

        # ----------------------------------------------
        # 6. Generate final report
        # ----------------------------------------------

        report_service = ReportService()

        report = report_service.generate_report(
            profile=extraction.profile,
            analysis=analysis,
        )

        # ----------------------------------------------
        # 7. Return complete response
        # ----------------------------------------------

        return {
            "filename": file.filename,
            "page_count": document["page_count"],
            "system_profile": (
                extraction.profile.model_dump()
            ),
            "user_evidence": [
                evidence.model_dump()
                for evidence
                in extraction.evidence
            ],
            "report": report.model_dump(),
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