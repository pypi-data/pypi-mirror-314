from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path

from typing import NoReturn


@dataclass
class DependencyManager:
    def __init__(self):
        self.__title = ''
        self.__address = ''
        self.__description = ''
        self.__manual_path = ''
        self.__application_start_date = datetime.now(UTC)

    def set_title(self, title: str) -> NoReturn:
        self.__title = title

    def set_description(self, description: str) -> NoReturn:
        self.__description = description

    def set_manual_path(self, manual_path: Path) -> NoReturn:
        self.__manual_path = manual_path

    def set_address(self, address: str) -> NoReturn:
        self.__address = address

    @property
    def application_start_date(self) -> datetime:
        return self.__application_start_date

    @property
    def title(self) -> str:
        return self.__title

    @property
    def description(self) -> str:
        return self.__description

    @property
    def address(self) -> str:
        return self.__address

    @property
    def manual_path(self) -> Path:
        return self.__manual_path


dm = DependencyManager()
