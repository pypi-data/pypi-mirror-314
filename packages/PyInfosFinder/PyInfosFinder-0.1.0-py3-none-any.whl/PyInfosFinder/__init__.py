from __future__ import annotations
from os import getenv

computerFuncs: int = 26
discordFuncs: int = 1
miscFuncs: int = 2
local: str | None = getenv('LOCALAPPDATA')
roaming: str | None = getenv('APPDATA')
__version__ = "0.0.1"
