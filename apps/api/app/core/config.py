from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str="development"
    ollama_base_url: str="http://127.0.0.1:11434"
    ollama_model: str="qwen3:4b"
    tavily_api_key: str | None=None
    youtube_api_key: str | None=None

    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings=Settings()
