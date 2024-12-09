import pathlib
import threading
from configparser import ConfigParser
from typing import Any
from cryptography.fernet import Fernet

lock: threading.RLock

class EnvConfig:
    _config_path: pathlib.Path
    _fernet: Fernet
    @classmethod
    def init_configer(cls) -> ConfigParser: ...
    @classmethod
    def sections(cls) -> str: ...
    @classmethod
    def read(cls, sections: str | list[str] | None = None, configer: ConfigParser | None = None) -> str: ...
    @classmethod
    def write(cls, section: str, force: bool = False, **kwargs: Any) -> None: ...
    @classmethod
    def delete(cls, section: str) -> None: ...
