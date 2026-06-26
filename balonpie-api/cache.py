import time
from dataclasses import dataclass
from typing import Any, Callable


class NoDataAvailableError(Exception):
    pass


@dataclass
class CacheEntry:
    value: Any
    fetched_at: float
    is_stale: bool


class TTLCache:
    def __init__(self, now_fn: Callable[[], float] = time.time):
        self._now = now_fn
        self._store: dict[str, tuple[float, Any]] = {}

    def get_or_refresh(
        self, key: str, ttl_seconds: float, fetch_fn: Callable[[], Any]
    ) -> CacheEntry:
        now = self._now()
        cached = self._store.get(key)
        if cached is not None:
            fetched_at, value = cached
            if now - fetched_at < ttl_seconds:
                return CacheEntry(value=value, fetched_at=fetched_at, is_stale=False)

        try:
            fresh_value = fetch_fn()
        except Exception:
            if cached is not None:
                fetched_at, value = cached
                return CacheEntry(value=value, fetched_at=fetched_at, is_stale=True)
            raise NoDataAvailableError(f"No data available for key '{key}'")

        self._store[key] = (now, fresh_value)
        return CacheEntry(value=fresh_value, fetched_at=now, is_stale=False)
