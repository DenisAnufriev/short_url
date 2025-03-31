import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None or DATABASE_URL.strip() == "":
    raise ValueError("❌ Ошибка: DATABASE_URL не установлен. Проверь .env файл!")

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """Создаёт сессию базы данных для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
