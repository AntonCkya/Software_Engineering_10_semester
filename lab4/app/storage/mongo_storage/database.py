from __future__ import annotations

from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection

from app.config import settings

class MongoDB:
    """Класс для работы с MongoDB"""

    _client = None
    _db = None

    @classmethod
    async def connect(cls):
        """Подключиться к MongoDB"""
        if cls._client is None:
            cls._client = MongoClient(
                host=settings.mongodb.host,
                port=settings.mongodb.port,
                username=settings.mongodb.user,
                password=settings.mongodb.password,
                authSource=settings.mongodb.auth_source,
            )
            cls._db = cls._client[settings.mongodb.db]

    @classmethod
    async def close(cls):
        """Закрыть соединение с MongoDB"""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None

    @classmethod
    def get_database(cls) -> Any:
        """Получить объект базы данных"""
        if cls._db is None:
            raise RuntimeError("MongoDB not connected. Call connect() first.")
        return cls._db

    @classmethod
    def get_collection(cls, name: str) -> Collection:
        """Получить объект коллекции"""
        db = cls.get_database()
        return db[name]
