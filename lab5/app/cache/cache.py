import asyncio
from collections import OrderedDict
from typing import Any, Optional


class AsyncLRUCache:
    """
    Асинхронный LRU-кэш с ограничением размера и временем жизни (TTL).
    """

    def __init__(self, maxsize: int, ttl: Optional[float] = None):
        if maxsize <= 0:
            raise ValueError("maxsize должен быть положительным целым числом")
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl должен быть положительным числом или None")

        self._maxsize: int = maxsize
        self._ttl: Optional[float] = ttl
        self._cache: OrderedDict[str, tuple[Any, Optional[float]]] = OrderedDict()
        self._lock: asyncio.Lock = asyncio.Lock()

    def _is_expired(self, expiration: Optional[float]) -> bool:
        if expiration is None:
            return False
        return asyncio.get_running_loop().time() >= expiration

    async def get(self, key: str, default: Any = None) -> Any:
        async with self._lock:
            if key not in self._cache:
                return default

            value, expiration = self._cache[key]
            if self._is_expired(expiration):
                del self._cache[key]
                return default

            self._cache.move_to_end(key)
            return value

    async def set(self, key: str, value: Any) -> None:
        async with self._lock:
            expiration = None
            if self._ttl is not None:
                expiration = asyncio.get_running_loop().time() + self._ttl

            if key in self._cache:
                del self._cache[key]

            self._cache[key] = (value, expiration)

            if len(self._cache) > self._maxsize:
                self._cache.popitem(last=False)

    async def delete(self, key: str) -> None:
        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        async with self._lock:
            self._cache.clear()

    async def expire(self) -> None:
        async with self._lock:
            expired_keys = [
                key for key, (_, exp) in self._cache.items()
                if self._is_expired(exp)
            ]
            for key in expired_keys:
                del self._cache[key]

    async def __contains__(self, key: str) -> bool:
        async with self._lock:
            if key not in self._cache:
                return False
            _, expiration = self._cache[key]
            if self._is_expired(expiration):
                del self._cache[key]
                return False
            return True

    async def __len__(self) -> int:
        await self.expire()
        async with self._lock:
            return len(self._cache)

    @property
    def maxsize(self) -> int:
        return self._maxsize

    @property
    def ttl(self) -> Optional[float]:
        return self._ttl
