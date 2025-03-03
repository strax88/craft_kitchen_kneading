from pydantic_settings import BaseSettings, SettingsConfigDict

from base_settings import PROJECT_DIR


__all__ = ["DB_CONFIG"]


class DBConfig(BaseSettings):
    """"""

    name: str = "main.db"
    url: str = f"sqlite+aiosqlite:///{name}"

    model_config = SettingsConfigDict(
        env_prefix="db_", env_file=f"{PROJECT_DIR}/main.env", env_file_encoding="utf-8", extra="ignore"
    )


DB_CONFIG = DBConfig()

if __name__ == "__main__":
    print(DB_CONFIG)
