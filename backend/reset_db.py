import sys
import os

# Ensure backend directory is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.database import engine, Base, SessionLocal
from app.main import init_db_schema, seed_initial_data

def reset_database():
    print("[INFO] Resetting database tables...")
    try:
        print("[INFO] Dropping existing schema tables...")
        Base.metadata.drop_all(bind=engine)
        print("[SUCCESS] All tables dropped.")
    except Exception as e:
        print(f"[WARNING] Could not drop all tables cleanly: {e}")

    print("[INFO] Recreating database schema tables...")
    init_db_schema()
    print("[SUCCESS] Database schema initialized.")

    print("[INFO] Seeding initial data...")
    seed_initial_data()
    print("[SUCCESS] Database reset and initial seeding completed successfully!")

if __name__ == "__main__":
    reset_database()
