import functools
from typing import Dict, Type
from app.cache.cache import AsyncLRUCache


def make_cached_repository(
    repo_class: Type,
    cache_config: Dict[str, dict]
) -> Type:
    """
    Фабрика, создающая класс-наследник repo_class с общим для всех экземпляров
    кэшированием указанных методов.

    :param repo_class: исходный асинхронный репозиторий
    :param cache_config: { 'method_name': {'maxsize': int, 'ttl': float, 'key_builder': callable} }
    :return: новый класс с кэшированием (кэши разделяются между экземплярами)
    """

    class CachedRepository(repo_class):
        _shared_caches: Dict[str, AsyncLRUCache] = {}
        _cache_config = cache_config

        def __new__(cls, *args, **kwargs):
            if not cls._shared_caches:
                cls._init_class_caches()
            return super().__new__(cls)

        @classmethod
        def _init_class_caches(cls):
            for method_name, config in cls._cache_config.items():
                cache = AsyncLRUCache(
                    maxsize=config.get('maxsize', 128),
                    ttl=config.get('ttl', None)
                )
                cls._shared_caches[method_name] = cache

                original_method = getattr(cls, method_name, None)
                if original_method is None:
                    raise AttributeError(
                        f"Method '{method_name}' not found in {cls.__name__}"
                    )
                key_builder = config.get('key_builder')
                setattr(cls, method_name, cls._make_cached_method(
                    original_method, cache, key_builder
                ))

        @staticmethod
        def _make_cached_method(method, cache: AsyncLRUCache, key_builder=None):
            @functools.wraps(method)
            async def cached_method(self, *args, **kwargs):
                if key_builder:
                    key = key_builder(self, *args, **kwargs)
                else:
                    key_parts = [
                        method.__name__,
                        str(args),
                        str(sorted(kwargs.items()))
                    ]
                    key = "|".join(key_parts)

                print(f"{method}: {cache}")
                cached_value = await cache.get(key)
                if cached_value is not None:
                    print(f"{method}: return cached")
                    return cached_value

                result = await method(self, *args, **kwargs)
                await cache.set(key, result)
                print(f"{method}: return non-cached")
                return result
            return cached_method

        @classmethod
        async def clear_all_caches(cls):
            for cache in cls._shared_caches.values():
                await cache.clear()

        @classmethod
        async def expire_all_caches(cls):
            for cache in cls._shared_caches.values():
                await cache.expire()

    return CachedRepository
