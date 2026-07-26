# Test script to see if connection to postgres database works using the SQLalchemy engine

from sqlalchemy import text

from src.database.database import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT version();"))

    print(result.scalar())  #simply returns the current version of the postgresql running