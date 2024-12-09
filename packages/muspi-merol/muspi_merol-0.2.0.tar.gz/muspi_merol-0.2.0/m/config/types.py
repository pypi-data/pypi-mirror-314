from typing import TypedDict


class Alias(TypedDict):
    cmd: str
    shell: bool


class Config(TypedDict):
    aliases: dict[str, Alias | str]
