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

    # Embedding Configuration
    EMBEDDING_PROVIDER:str
    EMBEDDING_MODEL:str
    EMBEDDING_DIMENSION:int
    
    # LLM Configuration
    LLM_PROVIDER: str
    LLM_MODEL: str
    
    # API Keys
    # Making them optional with an empty default lets you configure only the providers you're actually using.
    OPENAI_API_KEY: str = ""        #this makes sure that "" is the default value so we dont have to provide api keys for all simultaneously
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    VOYAGE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

# We import this object along with it's attributes wherever required to simply access the credentials
settings = Settings()