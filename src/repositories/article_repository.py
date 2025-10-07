from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.article import Article
from schemas.article_schema import ArticleCreate, ArticleFilters


class ArticleRepository(object):

    def __init__(self, db: Session):
        self.db = db

    def get_article_instance(self):
        return self.db.query(Article)

    def get_article_by_id(self, id):
        return self.db.query(Article).filter(Article.id == id).first()
    
    def get_article_by_author_filter(self, query, article_filters: ArticleFilters):
        return query.filter(Article.author.ilike(f"%{article_filters.author}%"))
    
    def get_article_by_tags_filter(self, query, tags_list: list):
        tag_filters = [Article.tags.ilike(f"%{tag}%") for tag in tags_list]
        return query.filter(or_(*tag_filters))

    def order_article_by_published(self, query):
        return query.order_by(Article.published_at.asc())
    
    def get_article_by_page_db(self, query, article_filters: ArticleFilters):
        return query.offset((article_filters.page - 1) * article_filters.size).limit(article_filters.size).all()
    
    def create(self, article: ArticleCreate):
        db_article = Article(**article.model_dump())
        self.db.add(db_article)
        self.db.commit()
        self.db.refresh(db_article)
        return db_article
    
    def update(self, db_article):
        self.db.commit()
        self.db.refresh(db_article)
        return db_article
    
    def delete(self, db_article):
        self.db.delete(db_article)
        self.db.commit()