import random
import string

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models
import schemas


def generate_short_id(length: int = 6):
    """
    Генерирует короткий уникальный идентификатор.

    :param length: Длина идентификатора, по умолчанию 6 символов.
    :return: Строка сгенерированного идентификатора.
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


async def create_url(db: AsyncSession, url_data: schemas.URLCreate):
    """
    Создает новый сокращенный URL и сохраняет его в базе данных.

    :param db: Асинхронная сессия базы данных.
    :param url_data: Данные о создаваемом URL.
    :return: Созданный объект URL.
    """
    print(f"🌍 Полученный URL: {url_data.original_url.encode('utf-8', 'ignore')}")
    new_url = models.URL(
        original_url=url_data.original_url, short_id=generate_short_id()
    )
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)
    return new_url


async def get_url_by_short_id(db: AsyncSession, short_id: str):
    """
    Получает URL по его короткому идентификатору.

    :param db: Асинхронная сессия базы данных.
    :param short_id: Короткий идентификатор URL.
    :return: Найденный объект URL или None, если не найден.
    """
    result = await db.execute(select(models.URL).where(models.URL.short_id == short_id))
    return result.scalar_one_or_none()


async def get_all_urls(db: AsyncSession):
    """
    Возвращает список всех сохраненных URL в базе данных.

    :param db: Асинхронная сессия базы данных.
    :return: Список объектов URL.
    """
    result = await db.execute(select(models.URL))
    return result.scalars().all()


async def update_url(db: AsyncSession, short_id: str, new_url: schemas.URLCreate):
    """
    Обновляет URL в базе данных по его короткому идентификатору.

    :param db: Асинхронная сессия базы данных.
    :param short_id: Короткий идентификатор URL.
    :param new_url: Новые данные для обновления.
    :return: Обновленный объект URL или None, если не найден.
    """
    db_url = await get_url_by_short_id(db, short_id)
    if db_url:
        db_url.original_url = new_url.original_url
        db_url.short_id = new_url.short_id
        await db.commit()
        await db.refresh(db_url)
        return db_url
    return None


async def delete_url(db: AsyncSession, short_id: str):
    """
    Удаляет URL из базы данных по его короткому идентификатору.

    :param db: Асинхронная сессия базы данных.
    :param short_id: Короткий идентификатор URL.
    :return: Удаленный объект URL или None, если не найден.
    """
    db_url = await get_url_by_short_id(db, short_id)
    if db_url:
        await db.delete(db_url)
        await db.commit()
        return db_url
    return None
