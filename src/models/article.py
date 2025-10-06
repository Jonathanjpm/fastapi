from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
import uuid


class ArticleGet(BaseModel):
    id: uuid.UUID
    title: str
    body: str
    tags: str
    author: str
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ArticleCreate(BaseModel):
    title: str
    body: str
    tags: str
    author: str
    published_at: Optional[datetime] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    tags: Optional[str] = None
    author: Optional[str] = None
    published_at: Optional[datetime] = None

class ArticleFilters(BaseModel):
    author: Optional[str] = None
    tags: Optional[str] = None
    page: int = 1
    size: int = 10