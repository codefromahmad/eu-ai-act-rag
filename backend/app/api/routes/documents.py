import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

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
from app.services.document_extraction_service import (
    DocumentExtractionService,
)
from app.services.file_validation_service import (
    FileValidationService,
)
from app.services.system_profile_service import (
    SystemProfileService,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


file_validation_service = FileValidationService()


def handle_llm_exception(
    exc: Exception,
) -> None:

    if isinstance(
        exc,
        LLMQuotaExceededError,
    ):
        raise HTTPException(
            status_code=503,
            detail=(
                "The AI service has temporarily exhausted "
                "its usage quota. Please try again later."
            ),
        )

    if isinstance(
        exc,
        LLMRateLimitError,
    ):
        raise HTTPException(
            status_code=429,
            detail=(
                "The AI service is receiving too many requests. "
                "Please try again shortly."
            ),
        )

    if isinstance(
        exc,
        LLMResponseError,
    ):
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service returned an invalid response."
            ),
        )

    if isinstance(
        exc,
        LLMServiceError,
    ):
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service is temporarily unavailable."
            ),
        )


def save_upload_to_temp(
    file: UploadFile,
    extension: str,
) -> str:

    with NamedTemporaryFile(
        suffix=extension,
        delete=False,
    ) as temp_file:

        shutil.copyfileobj(
            file.file,
            temp_file,
        )

        return temp_file.name


@router.post("/extract")
async def extract_document(
    file: UploadFile = File(...),
):

    extension = file_validation_service.validate(
        file
    )

    await file_validation_service.validate_size(
        file
    )

    temp_path = None

    try:
        temp_path = save_upload_to_temp(
            file=file,
            extension=extension,
        )

        extraction_service = (
            DocumentExtractionService()
        )

        document = await run_in_threadpool(
            extraction_service.extract,
            temp_path,
        )

        if not document.text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the document."
                ),
            )

        return {
            "filename": file.filename,
            "file_type": document.file_type,
            "page_count": document.page_count,
            "section_count": len(
                document.sections
            ),
            "text": document.text,
            "sections": [
                section.model_dump()
                for section in document.sections
            ],
        }

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to extract the document."
            ),
        )

    finally:
        if temp_path:
            Path(
                temp_path
            ).unlink(
                missing_ok=True
            )


@router.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
):

    extension = file_validation_service.validate(
        file
    )

    await file_validation_service.validate_size(
        file
    )

    temp_path = None

    try:
        temp_path = save_upload_to_temp(
            file=file,
            extension=extension,
        )

        extraction_service = (
            DocumentExtractionService()
        )

        document = await run_in_threadpool(
            extraction_service.extract,
            temp_path,
        )

        if not document.text.strip():
            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the document."
                ),
            )

        sections = [
            {
                "page_number": (
                    section.section_number
                ),
                "text": section.text,
            }
            for section in document.sections
        ]

        profile_service = (
            SystemProfileService()
        )

        extraction = await run_in_threadpool(
            profile_service.extract_profile,
            sections,
        )

        return {
            "filename": file.filename,
            "file_type": document.file_type,
            "page_count": document.page_count,
            "section_count": len(
                document.sections
            ),
            "system_profile": (
                extraction
                .profile
                .model_dump()
            ),
            "evidence": [
                item.model_dump()
                for item in extraction.evidence
            ],
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
        handle_llm_exception(
            exc
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while analyzing the document."
            ),
        )

    finally:
        if temp_path:
            Path(
                temp_path
            ).unlink(
                missing_ok=True
            )


@router.post("/report")
async def generate_compliance_report(
    file: UploadFile = File(...),
):

    extension = file_validation_service.validate(
        file
    )

    await file_validation_service.validate_size(
        file
    )

    temp_path = None
    db = None

    try:
        temp_path = save_upload_to_temp(
            file=file,
            extension=extension,
        )

        db = SessionLocal()

        pipeline = (
            CompliancePipelineService()
        )

        result = await run_in_threadpool(
            pipeline.analyze_document,
            db,
            temp_path,
            file.filename,
        )

        return {
            "analysis_id": result[
                "analysis_id"
            ],
            "filename": result[
                "filename"
            ],
            "file_type": result[
                "file_type"
            ],
            "page_count": result[
                "page_count"
            ],
            "section_count": result[
                "section_count"
            ],
            "system_profile": (
                result[
                    "system_profile"
                ].model_dump()
            ),
            "user_evidence": [
                evidence.model_dump()
                for evidence
                in result[
                    "user_evidence"
                ]
            ],
            "report": (
                result[
                    "report"
                ].model_dump()
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
        handle_llm_exception(
            exc
        )

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
            Path(
                temp_path
            ).unlink(
                missing_ok=True
            )