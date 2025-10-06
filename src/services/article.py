import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.constants import NOT_FOUND, WITHOUT_UPDATE
from utils.cache import cache
from repository.article import Article
from utils.validations import validate_unique_constrain, validate_content, validate_page
from models.article import ArticleCreate, ArticleUpdate, ArticleFilters, ArticleGet

def create_articles(db: Session, article: ArticleCreate) -> Article:
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
    

def update_articles(db: Session, id: uuid.UUID, article: ArticleUpdate) -> Article:
    db_article = db.query(Article).filter(Article.id == id).first()
    validate_content(db_article, NOT_FOUND)

    article = validate_unique_constrain(article, db_article)
    update_data = article.model_dump(exclude_unset=True, exclude_none=True)
    validate_content(update_data, WITHOUT_UPDATE)        

    for field, value in update_data.items():
        setattr(db_article, field, value)

    db.commit()
    db.refresh(db_article)
    cache.invalidate(str(id))

    return db_article


def get_articles(db: Session, id: uuid.UUID) -> Article:
    cached_article = cache.get(str(id))
    if cached_article:
        return cached_article
    
    article = db.query(Article).filter(Article.id == id).first()
    validate_content(article, NOT_FOUND)
    
    article_response = ArticleGet.model_validate(article)
    cache.set(str(id), article_response.model_dump())
    
    return article


def get_articles_filters(db: Session, article_filters: ArticleFilters):
    query = db.query(Article)
    
    if article_filters.author:
        query = query.filter(Article.author.ilike(f"%{article_filters.author}%"))
    
    if article_filters.tags:
        tags_list = [tag.strip() for tag in article_filters.tags.split(",")]
        tag_filters = [Article.tags.ilike(f"%{tag}%") for tag in tags_list]
        query = query.filter(or_(*tag_filters))

    query = query.order_by(Article.published_at.asc())
    validate_page(article_filters)
    articles = query.offset((article_filters.page - 1) * article_filters.size).limit(article_filters.size).all()
    validate_content(articles, NOT_FOUND)
    
    return articles


def delete_articles(db: Session, id: uuid.UUID):
    db_article = db.query(Article).filter(Article.id == id).first()
    validate_content(db_article, NOT_FOUND)
    
    db.delete(db_article)
    db.commit()