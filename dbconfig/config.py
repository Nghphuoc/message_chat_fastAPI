from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

#DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"  # Có thể đổi sang PostgreSQL, MySQL...

DATABASE_URL = "mysql://root:QKddluOjJFunHBUFoAoSZSIJJCoBVtsv@nozomi.proxy.rlwy.net:30138/railway"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,        # số kết nối mặc định trong pool
    max_overflow=20,     # số kết nối vượt quá pool_size
    pool_timeout=30,     # thời gian chờ nếu pool đầy
    pool_pre_ping=True   # kiểm tra kết nối sống trước khi dùng
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()