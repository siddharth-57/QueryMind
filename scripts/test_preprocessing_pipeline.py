from src.database.database import SessionLocal
from src.preprocessing.pipeline import EmailPreprocessingPipeline


db = SessionLocal()

try:
    pipeline = EmailPreprocessingPipeline(db)

    processed = pipeline.process()

    print(f"Processed {processed} email(s).")

finally:
    db.close()