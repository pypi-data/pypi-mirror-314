__all__ = [
    "AgentError",
    "AgentAuthError",
]


class AgentError(Exception):
    pass


class AgentAuthError(AgentError):
    pass
