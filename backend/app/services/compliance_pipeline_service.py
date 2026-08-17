from sqlalchemy.orm import Session

from app.models.report import ComplianceReport
from app.models.system_profile import SystemProfile
from app.services.full_analysis_service import FullAnalysisService
from app.services.pdf_service import PDFService
from app.services.report_service import ReportService
from app.services.system_profile_service import SystemProfileService


class CompliancePipelineService:

    def __init__(self):
        self.profile_service = SystemProfileService()
        self.analysis_service = FullAnalysisService()
        self.report_service = ReportService()

    def analyze_pdf(
        self,
        db: Session,
        file_path: str,
    ) -> dict:

        # ----------------------------------------------
        # 1. Extract PDF
        # ----------------------------------------------

        document = PDFService.extract_text(
            file_path
        )

        if not document["text"].strip():
            raise ValueError(
                "No readable text was found in the PDF."
            )

        # ----------------------------------------------
        # 2. Extract SystemProfile + evidence
        # ----------------------------------------------

        extraction = self.profile_service.extract_profile(
            pages=document["pages"]
        )

        # ----------------------------------------------
        # 3. Run risk-aware compliance analysis
        # ----------------------------------------------

        analysis = self.analysis_service.analyze(
            db=db,
            profile=extraction.profile,
            user_evidence=extraction.evidence,
        )

        # ----------------------------------------------
        # 4. Generate final report
        # ----------------------------------------------

        report = self.report_service.generate_report(
            profile=extraction.profile,
            analysis=analysis,
        )

        # ----------------------------------------------
        # 5. Return structured pipeline result
        # ----------------------------------------------

        return {
            "page_count": document["page_count"],
            "system_profile": extraction.profile,
            "user_evidence": extraction.evidence,
            "report": report,
        }