import uuid

from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, TIMESTAMP, Index, UniqueConstraint

from core.database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    tags = Column(Text, nullable=False)
    author = Column(String, nullable=False)
    published_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("title", "author", name="unique_title_author"),
        Index("idx_author", "author"),
        Index("idx_published_at", "published_at"),
    )
