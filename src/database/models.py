from sqlalchemy.orm import DeclarativeBase

# Every table in this project will inherit from this base.
# This is how SQLAlchemy will know which classes represent database tables.
class Base(DeclarativeBase):
    pass

