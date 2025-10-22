"""Caching utilities for the PyPI MCP server."""

import asyncio
import hashlib
import json
import logging
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional, TypeVar

from .config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class CacheEntry:
    """Metadata for cached values."""

    value: Any
    expires_at: float
    created_at: float
    last_accessed: float
    ttl: float


class AsyncTTLCache:
    """Thread-safe async cache with per-item TTL and LRU eviction."""

    def __init__(self, maxsize: int = 1000, ttl: float = 300.0) -> None:
        self._maxsize = maxsize
        self._default_ttl = ttl
        self._store: "OrderedDict[str, CacheEntry]" = OrderedDict()
        self._lock = asyncio.Lock()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expired = 0

    async def get(self, key: str) -> Optional[Any]:
        """Get item from cache if it exists and has not expired."""
        async with self._lock:
            self._purge_expired_locked()
            entry = self._store.get(key)
            if entry is None:
                self._misses += 1
                return None

            self._hits += 1
            now = time.monotonic()
            entry.last_accessed = now
            self._store.move_to_end(key)
            return entry.value

    async def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Set item in cache with optional TTL override."""
        async with self._lock:
            self._purge_expired_locked()

            if key in self._store:
                self._store.pop(key, None)

            effective_ttl = self._default_ttl if ttl is None else float(ttl)
            now = time.monotonic()
            expires_at = (
                now + effective_ttl if effective_ttl > 0 else float("inf")
            )

            self._store[key] = CacheEntry(
                value=value,
                created_at=now,
                last_accessed=now,
                ttl=effective_ttl,
                expires_at=expires_at,
            )
            self._store.move_to_end(key)
            self._evict_if_needed_locked()

    async def delete(self, key: str) -> None:
        """Delete item from cache."""
        async with self._lock:
            self._store.pop(key, None)

    async def clear(self) -> None:
        """Clear all items from cache."""
        async with self._lock:
            self._store.clear()
            self._hits = 0
            self._misses = 0
            self._evictions = 0
            self._expired = 0

    async def size(self) -> int:
        """Get current cache size (after purging expired entries)."""
        async with self._lock:
            self._purge_expired_locked()
            return len(self._store)

    async def stats(self) -> Dict[str, Any]:
        """Return cache statistics including size and eviction counts."""
        async with self._lock:
            self._purge_expired_locked()
            return {
                "hits": self._hits,
                "misses": self._misses,
                "evictions": self._evictions,
                "expired": self._expired,
                "size": len(self._store),
                "max_size": self._maxsize,
                "default_ttl": self._default_ttl,
            }

    async def touch(self, key: str) -> bool:
        """Refresh expiry of an existing cache key."""
        async with self._lock:
            self._purge_expired_locked()
            entry = self._store.get(key)
            if entry is None:
                return False

            now = time.monotonic()
            entry.last_accessed = now
            entry.expires_at = (
                now + entry.ttl if entry.ttl > 0 else float("inf")
            )
            self._store.move_to_end(key)
            return True

    async def purge_expired(self) -> int:
        """Purge expired entries and return the count removed."""
        async with self._lock:
            return self._purge_expired_locked()

    def _purge_expired_locked(self) -> int:
        now = time.monotonic()
        expired_keys = [
            key for key, entry in self._store.items() if entry.expires_at <= now
        ]
        for key in expired_keys:
            self._store.pop(key, None)
        if expired_keys:
            self._expired += len(expired_keys)
        return len(expired_keys)

    def _evict_if_needed_locked(self) -> None:
        while self._maxsize and len(self._store) > self._maxsize:
            self._store.popitem(last=False)
            self._evictions += 1


# Global cache instance
cache = AsyncTTLCache(maxsize=settings.cache_max_size, ttl=settings.cache_ttl)


def cache_key(*args: Any, **kwargs: Any) -> str:
    """Generate a cache key from arguments."""
    key_data = {"args": args, "kwargs": sorted(kwargs.items())}
    key_str = json.dumps(key_data, sort_keys=True, default=str)
    return hashlib.md5(key_str.encode()).hexdigest()


def cached(ttl: Optional[float] = None) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Decorator for caching async function results."""

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            # Generate cache key
            key = f"{func.__name__}:{cache_key(*args, **kwargs)}"

            # Try to get from cache
            cached_result = await cache.get(key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {key}")
                return cached_result  # type: ignore[no-any-return]

            # Execute function and cache result
            logger.debug(f"Cache miss for {key}")
            result = await func(*args, **kwargs)

            # Cache the result
            await cache.set(key, result, ttl=ttl)

            return result

        return wrapper

    return decorator


async def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    stats = await cache.stats()
    total_requests = stats["hits"] + stats["misses"]
    hit_rate = (stats["hits"] / total_requests) if total_requests else None
    return {
        "size": stats["size"],
        "max_size": stats["max_size"],
        "default_ttl": stats["default_ttl"],
        "hits": stats["hits"],
        "misses": stats["misses"],
        "requests": total_requests,
        "hit_rate": hit_rate,
        "evictions": stats["evictions"],
        "expired": stats["expired"],
    }
