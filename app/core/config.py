from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    APP_NAME: str = "API Licenciamento"
    APP_VERSION: str = "1.0.0"
    LICENSING_BASE_URL: str
    LICENSING_API_KEY: str
    

    model_config = SettingsConfigDict(env_file="app/.env", extra="ignore")
settings = Settings()