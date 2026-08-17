from app.db.database import Base, engine
from app.db.models.legal_chunk import LegalChunkDB


def init_db():
    Base.metadata.create_all(bind=engine)