from fastapi import APIRouter, HTTPException

from app.db.database import SessionLocal
from app.repositories.analysis_repository import (
    AnalysisRepository,
)


router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"],
)


@router.get("")
def get_all_analyses():

    db = SessionLocal()

    try:
        analyses = AnalysisRepository.get_all(
            db=db
        )

        return [
            {
                "analysis_id": analysis.analysis_id,
                "filename": analysis.filename,
                "file_type": analysis.file_type,
                "risk_category": analysis.risk_category,
                "compliance_score": (
                    analysis.compliance_score
                ),
                "coverage": analysis.coverage,
                "created_at": analysis.created_at,
            }
            for analysis in analyses
        ]

    finally:
        db.close()


@router.get("/{analysis_id}")
def get_analysis(
    analysis_id: str,
):

    db = SessionLocal()

    try:
        analysis = (
            AnalysisRepository.get_by_analysis_id(
                db=db,
                analysis_id=analysis_id,
            )
        )

        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found.",
            )

        return {
            "analysis_id": analysis.analysis_id,
            "filename": analysis.filename,
            "file_type": analysis.file_type,
            "risk_category": analysis.risk_category,
            "compliance_score": (
                analysis.compliance_score
            ),
            "coverage": analysis.coverage,
            "system_profile": (
                analysis.system_profile
            ),
            "report": analysis.report,
            "created_at": analysis.created_at,
        }

    finally:
        db.close()