import logging
import time

from sqlalchemy.orm import Session

from app.repositories.analysis_repository import (
    AnalysisRepository,
)
from app.services.document_extraction_service import (
    DocumentExtractionService,
)
from app.services.full_analysis_service import FullAnalysisService
from app.services.report_service import ReportService
from app.services.system_profile_service import SystemProfileService


logger = logging.getLogger(__name__)


class CompliancePipelineService:

    def __init__(self):
        self.document_extraction_service = (
            DocumentExtractionService()
        )

        self.profile_service = SystemProfileService()
        self.analysis_service = FullAnalysisService()
        self.report_service = ReportService()

    def analyze_document(
        self,
        db: Session,
        file_path: str,
        original_filename: str | None = None,
    ) -> dict:

        pipeline_start = time.perf_counter()

        logger.info("[REPORT] Pipeline started")

        # --------------------------------------------------
        # 1. Document extraction
        # --------------------------------------------------

        stage_start = time.perf_counter()

        document = (
            self.document_extraction_service.extract(
                file_path=file_path
            )
        )

        logger.info(
            "[REPORT] Document extraction complete in %.2fs",
            time.perf_counter() - stage_start,
        )

        if not document.text.strip():
            raise ValueError(
                "No readable text was found in the document."
            )

        sections = [
            {
                "source_type": (
                    "page"
                    if document.file_type == "pdf"
                    else "section"
                ),
                "source_number": section.section_number,
                "text": section.text,
            }
            for section in document.sections
        ]

        # --------------------------------------------------
        # 2. System profile extraction
        # --------------------------------------------------

        logger.info("[REPORT] Starting system profile extraction")

        stage_start = time.perf_counter()

        extraction = (
            self.profile_service.extract_profile(
                pages=sections
            )
        )

        logger.info(
            "[REPORT] System profile extraction complete in %.2fs",
            time.perf_counter() - stage_start,
        )

        # --------------------------------------------------
        # 3. Compliance analysis
        # --------------------------------------------------

        logger.info("[REPORT] Starting compliance analysis")

        stage_start = time.perf_counter()

        analysis = self.analysis_service.analyze(
            db=db,
            profile=extraction.profile,
            user_evidence=extraction.evidence,
        )

        logger.info(
            "[REPORT] Compliance analysis complete in %.2fs",
            time.perf_counter() - stage_start,
        )

        # --------------------------------------------------
        # 4. Report generation
        # --------------------------------------------------

        logger.info("[REPORT] Starting report generation")

        stage_start = time.perf_counter()

        report = self.report_service.generate_report(
            profile=extraction.profile,
            analysis=analysis,
        )

        logger.info(
            "[REPORT] Report generation complete in %.2fs",
            time.perf_counter() - stage_start,
        )

        # --------------------------------------------------
        # 5. Persistence
        # --------------------------------------------------

        logger.info("[REPORT] Starting database save")

        stage_start = time.perf_counter()

        saved_analysis = AnalysisRepository.save(
            db=db,
            filename=(
                original_filename
                or document.filename
            ),
            file_type=document.file_type,
            profile=extraction.profile,
            report=report,
        )

        logger.info(
            "[REPORT] Database save complete in %.2fs",
            time.perf_counter() - stage_start,
        )

        logger.info(
            "[REPORT] Pipeline complete in %.2fs",
            time.perf_counter() - pipeline_start,
        )

        return {
            "analysis_id": saved_analysis.analysis_id,
            "filename": (
                original_filename
                or document.filename
            ),
            "file_type": document.file_type,
            "page_count": document.page_count,
            "section_count": len(document.sections),
            "system_profile": extraction.profile,
            "user_evidence": extraction.evidence,
            "report": report,
        }