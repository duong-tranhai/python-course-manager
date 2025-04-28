from app.database import SessionLocal
from sqlalchemy import text

def test_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # Simple test query
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:")
        print(e)
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()
