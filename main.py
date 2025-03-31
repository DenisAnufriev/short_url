from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import models
import schemas
from database import SessionLocal
from database import engine

app = FastAPI(
    title="URL Short API",
    description="Сервис для сокращения ссылок на FastAPI",
    version="1.0.0",
    contact={
        "name": "AD",
        "email": "test@example.com",
    },
)


async def create_tables():
    """Создание таблиц в базе данных при старте приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("startup")
async def startup():
    """Обработчик события запуска приложения."""
    await create_tables()


async def get_db():
    """Создаёт сессию базы данных для каждого запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.post("/", response_model=schemas.URLResponse, status_code=201)
async def shorten_url(url_data: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    """Создаёт короткую ссылку для переданного URL.

    Args:
        url_data (schemas.URLCreate): Данные с оригинальным URL.
        db (AsyncSession): Сессия базы данных.

    Returns:
        dict: Сокращённый URL и оригинальный URL.
    """
    db_url = await crud.create_url(db=db, url_data=url_data)
    return {
        "short_url": f"http://127.0.0.1:8080/{db_url.short_id}",
        "original_url": db_url.original_url,
    }


@app.get("/{short_id}")
async def redirect_to_original(short_id: str, db: AsyncSession = Depends(get_db)):
    """Перенаправляет пользователя на оригинальный URL по короткому ID.

    Args:
        short_id (str): Короткий идентификатор URL.
        db (AsyncSession): Сессия базы данных.

    Returns:
        RedirectResponse: Перенаправление на оригинальный URL.
    """
    db_url = await crud.get_url_by_short_id(db=db, short_id=short_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    if not db_url.original_url.startswith(("http://", "https://")):
        full_url = f"http://{db_url.original_url}"
    else:
        full_url = db_url.original_url

    print(f"Редирект на: {full_url}")
    return RedirectResponse(url=full_url, status_code=307)


@app.get("/urls/", response_model=list[schemas.URLResponse])
async def get_urls(db: AsyncSession = Depends(get_db)):
    """Получает список всех сохранённых URL.

    Args:
        db (AsyncSession): Сессия базы данных.

    Returns:
        list[schemas.URLResponse]: Список всех сокращённых ссылок.
    """
    db_urls = await crud.get_all_urls(db=db)
    return [
        schemas.URLResponse(
            short_url=f"http://127.0.0.1:8080/{url.short_id}",
            original_url=url.original_url,
        )
        for url in db_urls
    ]
