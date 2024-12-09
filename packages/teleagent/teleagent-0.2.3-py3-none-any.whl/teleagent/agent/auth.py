import typing as tp
from contextlib import asynccontextmanager

if tp.TYPE_CHECKING:
    from .agent import TelegramAgent


class AuthMixin:
    async def start_session(self: "TelegramAgent") -> None:
        if not self.client.is_connected():
            await self.client.connect()

    async def stop_session(self: "TelegramAgent") -> None:
        if self.client.is_connected():
            await self.client.disconnect()

    @asynccontextmanager
    async def session(self: "TelegramAgent") -> tp.AsyncGenerator[None, None]:
        await self.start_session()
        try:
            yield
        finally:
            await self.stop_session()
