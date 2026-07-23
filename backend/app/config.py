from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ICU_API_KEY: str
    ICU_ATHLETE_ID: str

    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_VERSION: str

    COSMOS_ENDPOINT: str
    COSMOS_KEY: str
    COSMOS_DATABASE: str

    ENV: str = "local"


settings = Settings()
