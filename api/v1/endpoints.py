from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from core.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.URLResponse, status_code=201)
async def shorten_url(url_data: schemas.URLCreate, db: AsyncSession = Depends(get_db)):
    """Создаёт короткую ссылку для переданного URL."""
    db_url = await crud.create_url(db=db, url_data=url_data)
    return {
        "short_url": f"http://127.0.0.1:8080/{db_url.short_id}",
        "original_url": db_url.original_url,
    }


@router.get("/{short_id}")
async def redirect_to_original(short_id: str, db: AsyncSession = Depends(get_db)):
    """Перенаправляет пользователя на оригинальный URL по короткому ID."""
    db_url = await crud.get_url_by_short_id(db=db, short_id=short_id)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")

    full_url = db_url.original_url
    if not full_url.startswith(("http://", "https://")):
        full_url = f"http://{full_url}"

    print(f"Редирект на: {full_url}")
    return RedirectResponse(url=full_url, status_code=307)


@router.get("/urls/", response_model=list[schemas.URLResponse])
async def get_urls(db: AsyncSession = Depends(get_db)):
    """Получает список всех сохранённых URL."""
    db_urls = await crud.get_all_urls(db=db)
    return [
        schemas.URLResponse(
            short_url=f"http://127.0.0.1:8080/{url.short_id}",
            original_url=url.original_url,
        )
        for url in db_urls
    ]