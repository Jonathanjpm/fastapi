import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.article_schema import ArticleCreate, ArticleUpdate, ArticleFilters
from services.article_service import ArticleService
from repositories.article_repository import ArticleRepository

def get_article_service(db = Depends(get_db)):
    user_repository = ArticleRepository(db)
    return ArticleService(user_repository)

router = APIRouter()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_article(id: uuid.UUID, article_service: ArticleService = Depends(get_article_service)):
    return article_service.get_articles(id)


@router.get("/", status_code=status.HTTP_200_OK)
def get_article_filters(article_filters: ArticleFilters = Depends(), article_service: ArticleService = Depends(get_article_service)):
    return article_service.get_articles_filters(article_filters)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate, article_service: ArticleService = Depends(get_article_service)):
    return article_service.create_articles(article)


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_article(id: uuid.UUID, article: ArticleUpdate, article_service: ArticleService = Depends(get_article_service)):
    return article_service.update_articles(id, article)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: uuid.UUID, article_service: ArticleService = Depends(get_article_service)):
    return article_service.delete_articles(id)