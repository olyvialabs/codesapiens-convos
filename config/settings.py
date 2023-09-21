from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    OPENAI_API_KEY: str = None
    OPENAI_MODEL = "gpt-3.5-turbo"  # can be gpt4
    output_folder = "outputs"
    temp_folder = "temp"


path = Path(__file__).parent.parent.absolute()
settings = Settings(_env_file=path.joinpath(
    ".env"), _env_file_encoding="utf-8")
