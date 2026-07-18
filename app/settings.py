from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str
    session_expire_days: int
    
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()