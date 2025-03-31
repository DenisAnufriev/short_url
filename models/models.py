from sqlalchemy import Column, Integer, String, Text

from core.database import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_id = Column(String(6), unique=True, index=True)
    original_url = Column(Text, nullable=False)
