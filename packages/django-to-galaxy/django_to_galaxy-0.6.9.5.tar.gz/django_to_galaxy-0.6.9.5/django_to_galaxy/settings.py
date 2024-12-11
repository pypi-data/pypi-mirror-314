from pydantic import BaseSettings


class Settings(BaseSettings):
    GALAXY_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


settings = Settings()
