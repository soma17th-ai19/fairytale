from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    llm_provider: str = "fake"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"

    solar_api_key: str = ""
    solar_base_url: str = "https://api.upstage.ai/v1/solar"
    solar_model: str = "solar-pro"


settings = Settings()
