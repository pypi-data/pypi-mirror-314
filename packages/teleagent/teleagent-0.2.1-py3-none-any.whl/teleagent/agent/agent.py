from .auth import AuthMixin
from .base import TelegramAgentBase


class TelegramAgent(AuthMixin, TelegramAgentBase):
    pass
