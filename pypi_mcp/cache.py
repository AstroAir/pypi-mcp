"""Caching utilities for the PyPI MCP server."""

import asyncio
import hashlib
import json
import logging
from typing import Any, Callable, Optional, TypeVar

from cachetools import TTLCache

from .config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


class AsyncTTLCache:
    """Thread-safe async TTL cache implementation."""

    def __init__(self, maxsize: int = 1000, ttl: int = 300):
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache."""
        async with self._lock:
            return self._cache.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Set item in cache."""
        async with self._lock:
            self._cache[key] = value

    async def delete(self, key: str) -> None:
        """Delete item from cache."""
        async with self._lock:
            self._cache.pop(key, None)

    async def clear(self) -> None:
        """Clear all items from cache."""
        async with self._lock:
            self._cache.clear()

    async def size(self) -> int:
        """Get current cache size."""
        async with self._lock:
            return len(self._cache)


# Global cache instance
cache = AsyncTTLCache(maxsize=settings.cache_max_size, ttl=settings.cache_ttl)


def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    key_data = {"args": args, "kwargs": sorted(kwargs.items())}
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl: Optional[int] = None):
    """Decorator for caching async function results."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"

            # Try to get from cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {key}")
                return cached_result

            # Execute function and cache result
            logger.debug(f"Cache miss for {key}")
            result = await func(*args, **kwargs)

            # Cache the result
            await cache.set(key, result)

            return result

        return wrapper

    return decorator


async def get_cache_stats() -> dict:
    """Get cache statistics."""
    size = await cache.size()
    return {
        "size": size,
        "max_size": settings.cache_max_size,
        "ttl": settings.cache_ttl,
        "hit_rate": "N/A",  # Would need to track hits/misses for this
    }
