from fastapi import FastAPI
from routers import article
from core.exceptions import integrity_error_handler, internal_error_server
from sqlalchemy.exc import IntegrityError
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, internal_error_server)
app.include_router(article.router, prefix="/articles")
