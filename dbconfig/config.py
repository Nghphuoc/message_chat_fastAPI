from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.getenv("ENV_FILE", ".env.prod"))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
NAME_DB= os.getenv("NAME_DB")
DATABASE_URL = f"{NAME_DB}{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Có thể đổi sang PostgreSQL, MySQL...

# DATABASE_URL = "mysql+pymysql://root:QKddluOjJFunHBUFoAoSZSIJJCoBVtsv@nozomi.proxy.rlwy.net:30138/railway"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()