from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_NAME = getenv("DATABASE_NAME")
DB_PASSWORD = getenv("DATABASE_PASSWORD")
DB_PORT = getenv("DATABASE_PORT")
DB_PROVIDER = getenv("DATABASE_PROVIDER")
DB_URL = (
    f"postgresql://postgres:{DB_PASSWORD}@db.{DB_NAME}.{DB_PROVIDER}:{DB_PORT}/postgres"
)

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
