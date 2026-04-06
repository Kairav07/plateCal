from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str | None = None
    openai_model: str = 'gpt-4.1-mini'
    usda_api_key: str | None = None
    allowed_origin: str = 'http://localhost:5173'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
