# All required variables are stored here in one place

from pydantic_settings import BaseSettings, SettingsConfigDict

# BaseSettings: Tells the class to use environment variables
class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    QDRANT_URL:str
    QDRANT_COLLECTION:str

    EMBEDDING_PROVIDER:str
    EMBEDDING_MODEL:str
    EMBEDDING_DIMENSION:int

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# We import this object along with it's attributes wherever required to simply access the credentials
settings = Settings()