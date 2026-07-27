from src.database.database import SessionLocal
from src.ingestion.sync_service import SyncService


def main():
    db = SessionLocal()

    try:
        service = SyncService(db)
        service.sync()
    finally:
        db.close()


if __name__ == "__main__":
    main()