from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData
from core.config import host, port,user, password, name, schema

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{name}"

engine = create_engine(DATABASE_URL)
metadata = MetaData(schema=schema)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base(metadata=metadata)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()