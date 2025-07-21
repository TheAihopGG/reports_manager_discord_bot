from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


__all__ = ("BaseModel",)
