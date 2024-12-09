import abc
import typing as tp

from telethon import TelegramClient, sessions

from ..types import AppType, ProxyType

if tp.TYPE_CHECKING:
    from .agent import TelegramAgent


class TelegramAgentBase(abc.ABC):
    def __init__(
        self: "TelegramAgent",
        session: sessions.Session,
        app: AppType,
        *,
        proxy: ProxyType | None = None,
        **kwargs: tp.Any,
    ) -> None:
        telegram_client_kwargs: dict[str, tp.Any] = {}

        if app is not None:
            kwargs.update(app)

        lang_pack: str | None = kwargs.pop("lang_pack")

        if proxy is not None:
            kwargs["proxy"] = dict(proxy)

        telegram_client_kwargs.update(kwargs)

        self._client = TelegramClient(session, **telegram_client_kwargs)

        if lang_pack is not None:
            self._client._init_request.lang_pack = lang_pack  # noqa

    @property
    def client(self: "TelegramAgent") -> TelegramClient:
        return self._client
