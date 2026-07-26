from sqlalchemy import create_engine

from src.config.settings import settings


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOST}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
)

# Does not immediately connect to PostgreSQL. It simply prepares the engine.
# SQLAlchemy opens an actual connection only when one is needed.
engine = create_engine(DATABASE_URL)