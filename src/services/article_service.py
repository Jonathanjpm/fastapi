import uuid

from core.constants import NOT_FOUND, WITHOUT_UPDATE
from utils.cache import cache
from utils.validations import validate_unique_constrain, validate_content, validate_page
from schemas.article_schema import  ArticleCreate, ArticleUpdate, ArticleFilters, ArticleGet
from repositories.article_repository import ArticleRepository
from core.exceptions import InvalidOptionFilterException


class ArticleService():

    def __init__(self, article_repository: ArticleRepository):
        self.article_repository = article_repository

    def create_articles(self, article: ArticleCreate):
        return self.article_repository.create(article)

    def get_articles(self, id: uuid.UUID):
        cached_article = cache.get(str(id))
        if cached_article:
            return cached_article
        
        article =self.article_repository.get_article_by_id(id)
        validate_content(article, NOT_FOUND)
        
        article_response = ArticleGet.model_validate(article)
        cache.set(str(id), article_response.model_dump())
        
        return article
    
    def get_articles_filters(self, article_filters: ArticleFilters):
        query = self.article_repository.get_article_instance()
        
        if article_filters.author:
            query = self.article_repository.get_article_by_author_filter(query, article_filters)
        
        if article_filters.tags and query.count() == 0:
            query = self.article_repository.get_article_instance()
            tags_list = [tag.strip() for tag in article_filters.tags.split(",")]
            query = self.article_repository.get_article_by_tags_filter(query, tags_list)
        
        if not article_filters.author and not article_filters.tags:
            raise InvalidOptionFilterException

        query = self.article_repository.order_article_by_published(query)
        validate_page(article_filters)
        articles = self.article_repository.get_article_by_page_db(query, article_filters)
        validate_content(articles, NOT_FOUND)
        
        return articles    

    def update_articles(self, id: uuid.UUID, article: ArticleUpdate):
        db_article = self.article_repository.get_article_by_id(id)
        validate_content(db_article, NOT_FOUND)

        article = validate_unique_constrain(article, db_article)
        update_data = article.model_dump(exclude_unset=True, exclude_none=True)
        validate_content(update_data, WITHOUT_UPDATE)        

        for field, value in update_data.items():
            setattr(db_article, field, value)

        db_article = self.article_repository.update(db_article)
        cache.invalidate(str(id))

        return db_article

    def delete_articles(self, id: uuid.UUID):
        db_article = self.article_repository.get_article_by_id(id)
        validate_content(db_article, NOT_FOUND)
        self.article_repository.delete(db_article)