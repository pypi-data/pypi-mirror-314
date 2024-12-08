import typing as tp

__all__ = ["AppType"]


class AppType(tp.TypedDict):
    api_id: int
    api_hash: str
    device_model: str
    system_version: str
    app_version: str
    lang_code: str
    system_lang_code: str
    lang_pack: str
