from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    OPENAI_API_KEY: str = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"  # can be gpt4
    output_folder: str = "outputs"
    temp_folder: str = "temp"
    SUPABASE_URL: str = None
    SUPABASE_KEY: str = None
    CROSS_ORIGIN_SERVICE_SECRET: str = None
    GITHUB_APP_ID_NUMBER: str = None


path = Path(__file__).parent.parent.absolute()
settings = Settings(_env_file=path.joinpath(
    ".env"), _env_file_encoding="utf-8")
