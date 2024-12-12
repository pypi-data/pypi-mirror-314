import json
from json import JSONDecodeError
from pathlib import Path

from pydantic import PositiveInt, StrictStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    def __init__(self):
        super().__init__()
        self.serialize_url_map()

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=Path(__file__).parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )
    DEFAULT_CONNECTOR_TIMEOUT: PositiveInt | None = 120
    API_PREFIX: StrictStr | None = "/api/integra"
    URL_PATH_MAPPER: StrictStr | None = ""

    def serialize_url_map(self):
        if self.URL_PATH_MAPPER:
            try:
                self.URL_PATH_MAPPER = json.loads(self.URL_PATH_MAPPER)
            except JSONDecodeError:
                self.URL_PATH_MAPPER = {}
        else:
            self.URL_PATH_MAPPER = {}


SETTINGS = Settings()
