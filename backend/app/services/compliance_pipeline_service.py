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

        document = (
            self.document_extraction_service.extract(
                file_path=file_path
            )
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

        extraction = (
            self.profile_service.extract_profile(
                pages=sections
            )
        )

        analysis = self.analysis_service.analyze(
            db=db,
            profile=extraction.profile,
            user_evidence=extraction.evidence,
        )

        report = self.report_service.generate_report(
            profile=extraction.profile,
            analysis=analysis,
        )

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