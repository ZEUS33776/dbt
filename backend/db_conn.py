from database import SessionLocal, engine
from sqlalchemy import text

def test_connection():
    # Create a session
    db = SessionLocal()
    try:
        # Simple test query
        test_query = text("SELECT @@VERSION as version")
        result = db.execute(test_query)
        version = result.scalar()
        print("Successfully connected to database!")
        print(f"SQL Server version: {version}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()