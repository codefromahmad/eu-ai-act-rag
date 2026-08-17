from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    JSON,
    String,
    Text,
)

from app.db.database import Base


class AnalysisDB(Base):
    __tablename__ = "analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    analysis_id = Column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    file_type = Column(
        String,
        nullable=False,
    )

    risk_category = Column(
        String,
        nullable=True,
        index=True,
    )

    compliance_score = Column(
        Float,
        nullable=True,
    )

    coverage = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    system_profile = Column(
        JSON,
        nullable=False,
    )

    report = Column(
        JSON,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )