from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent
APPS_DIR = Path(__file__).parent
BASE_DIR = APPS_DIR


class ServicesBaseURL(BaseSettings):
    """"""
    auth: str = "http://127.0.0.1:8000"
    user: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=f"{PROJECT_DIR}/main.env", env_prefix="service_base_url_", extra="ignore")

SERVICES_BASE_URL = ServicesBaseURL()