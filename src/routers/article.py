import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from models.article import ArticleCreate, ArticleUpdate, ArticleFilters
from services.article import get_articles_filters, get_articles
from services.article import create_articles, update_articles, delete_articles



router = APIRouter()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_article(id: uuid.UUID, db: Session = Depends(get_db)):
    return get_articles(db, id)


@router.get("/", status_code=status.HTTP_200_OK)
def get_article_filters(article_filters: ArticleFilters = Depends(), db: Session = Depends(get_db)):
    return get_articles_filters(db, article_filters)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_articles(db, article)


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_article(id: uuid.UUID, article: ArticleUpdate, db: Session = Depends(get_db)):
    return update_articles(db, id, article)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: uuid.UUID, db: Session = Depends(get_db)):
    return delete_articles(db, id)