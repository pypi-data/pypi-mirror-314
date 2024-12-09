import typing as tp

__all__ = ["ProxyType"]


class ProxyType(tp.TypedDict):
    proxy_type: int | str
    addr: str
    port: int
    rdns: bool
    username: str | None
    password: str | None
