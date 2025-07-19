from sqlalchemy import create_engine

# app/models/base.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
DATABASE_URL = "sqlite:///gaceta1.db"
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # Increase the pool size
    max_overflow=20,  # Increase the overflow size
    pool_timeout=30,  # Adjust timeout as needed
    pool_recycle=1800,  # Adjust recycle time as needed
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
