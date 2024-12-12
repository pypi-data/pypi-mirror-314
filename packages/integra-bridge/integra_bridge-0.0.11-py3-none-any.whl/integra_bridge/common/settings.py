import json
from json import JSONDecodeError
from pathlib import Path

from pydantic import PositiveInt, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DEFAULT_CONNECTOR_TIMEOUT: PositiveInt = 120
    API_PREFIX: StrictStr = "/api/integra"
    URL_PATH_MAPPER: StrictStr | None = ""

    def serialize_url_map(self):
        if SETTINGS.URL_PATH_MAPPER:
            try:
                SETTINGS.URL_PATH_MAPPER = json.loads(SETTINGS.URL_PATH_MAPPER)
            except JSONDecodeError:
                SETTINGS.URL_PATH_MAPPER = {}


SETTINGS = Settings()
SETTINGS.serialize_url_map()
