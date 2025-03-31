from pydantic import BaseModel


class URLBase(BaseModel):
    original_url: str

    class Config:
        orm_mode = True


class URLCreate(URLBase):
    """Схема для создания нового URL"""
    pass


class URLResponse(URLBase):
    """Схема для ответа с данными URL, включая сокращённую ссылку"""

    short_url: str
