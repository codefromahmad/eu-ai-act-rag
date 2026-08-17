import uuid

from sqlalchemy.orm import Session

from app.db.models.analysis import AnalysisDB
from app.models.report import ComplianceReport
from app.models.system_profile import SystemProfile


class AnalysisRepository:

    @staticmethod
    def save(
        db: Session,
        filename: str,
        file_type: str,
        profile: SystemProfile,
        report: ComplianceReport,
    ) -> AnalysisDB:

        analysis = AnalysisDB(
            analysis_id=str(
                uuid.uuid4()
            ),
            filename=filename,
            file_type=file_type,
            risk_category=(
                report
                .risk_classification
                .category
                .value
            ),
            compliance_score=(
                report
                .score
                .compliance_score
            ),
            coverage=(
                report
                .score
                .coverage
            ),
            system_profile=(
                profile.model_dump()
            ),
            report=(
                report.model_dump(
                    mode="json"
                )
            ),
        )

        db.add(
            analysis
        )

        db.commit()

        db.refresh(
            analysis
        )

        return analysis

    @staticmethod
    def get_by_analysis_id(
        db: Session,
        analysis_id: str,
    ) -> AnalysisDB | None:

        return (
            db.query(
                AnalysisDB
            )
            .filter(
                AnalysisDB.analysis_id
                == analysis_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
    ) -> list[AnalysisDB]:

        return (
            db.query(
                AnalysisDB
            )
            .order_by(
                AnalysisDB.created_at.desc()
            )
            .all()
        )