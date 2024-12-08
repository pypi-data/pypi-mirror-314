import abc
import asyncio
import functools
import math
import time
import typing as tp
from contextlib import asynccontextmanager
from datetime import timedelta

try:
    from redis.asyncio import Redis
except ImportError:
    Redis = None  # type: ignore[misc,assignment]

__all__ = [
    "RateLimitMemory",
    "RateLimitRedis",
    "RateLimitHandler",
]

_F = tp.TypeVar("_F", bound=tp.Callable[..., tp.Awaitable[tp.Any]])


class RateLimit(abc.ABC):
    def __init__(self, function_name: str, ex_time: timedelta) -> None:
        self._function_name = function_name
        self._ex_time = int(ex_time.total_seconds())

    @abc.abstractmethod
    async def set(self, slug: str) -> None:
        pass

    @abc.abstractmethod
    async def get_seconds(self, slug: str) -> int | None:
        pass


class RateLimitMemory(RateLimit):
    @tp.override
    def __init__(self, function_name: str, ex_time: timedelta) -> None:
        super().__init__(function_name, ex_time)

        self._storage: dict[str, float] = {}

    async def set(self, slug: str) -> None:
        expires_at = time.time() + self._ex_time
        self._storage[slug] = expires_at

    async def get_seconds(self, slug: str) -> int | None:
        current_time = time.time()
        expires_at = self._storage.get(slug)

        if expires_at is None:
            return None

        if current_time > expires_at:
            del self._storage[slug]
            return None

        return math.ceil(expires_at - current_time)


class RateLimitRedis(RateLimit):
    _key_prefix: str = "rate_limit"

    @tp.override
    def __init__(self, function_name: str, ex_time: timedelta, *, redis_client: Redis) -> None:
        super().__init__(function_name, ex_time)

        self._redis_client = redis_client

    async def set(self, slug: str) -> None:
        await self._redis_client.set(self._build_key(slug), 0, ex=self._ex_time)

    async def get_seconds(self, slug: str) -> int | None:
        ttl = await self._redis_client.ttl(self._build_key(slug))
        return ttl if ttl > 0 else None

    def _build_key(self, slug: str) -> str:
        return f"{self._key_prefix}:{self._function_name}:{slug}"


class RateLimitHandler:
    def __init__(self, slug: str) -> None:
        self._slug = slug

    @asynccontextmanager
    async def handle(self, rate_limit: RateLimit) -> tp.AsyncGenerator[None, None]:
        seconds = await rate_limit.get_seconds(self._slug)
        if seconds is not None:
            await asyncio.sleep(seconds)

        try:
            yield
        finally:
            await rate_limit.set(self._slug)

    def decorate(self, rate_limit: RateLimit) -> tp.Callable[[_F], _F]:
        def decorator(func: _F) -> _F:
            @functools.wraps(func)
            async def wrapper(*args: tp.Any, **kwargs: tp.Any) -> tp.Any:
                async with self.handle(rate_limit):
                    return await func(*args, **kwargs)

            return tp.cast(_F, wrapper)

        return decorator
