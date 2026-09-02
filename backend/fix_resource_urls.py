from app.db.database import SessionLocal
from app.models.models import LearningResource

URL_UPDATES = {
    1: "https://www.igotkarmayogi.gov.in/",
    2: "https://www.igotkarmayogi.gov.in/",
    3: "https://www.igotkarmayogi.gov.in/",
    4: "https://www.mospi.gov.in/training-programmes/jts-induction-training",
    5: "https://www.mospi.gov.in/training-programmes/jts-induction-training",
    6: "https://www.mospi.gov.in/training-programmes/jts-induction-training",
    7: "https://www.mospi.gov.in/web/mospi/data",
    8: "https://www.mospi.gov.in/",
    9: "https://www.mospi.gov.in/",
}

db = SessionLocal()

try:
    for resource_id, new_url in URL_UPDATES.items():
        resource = db.query(LearningResource).filter(
            LearningResource.id == resource_id
        ).first()

        if resource:
            print(f"Updating #{resource.id}: {resource.title}")
            print(f"OLD: {resource.official_url}")
            print(f"NEW: {new_url}")
            resource.official_url = new_url

    db.commit()
    print("\nResource URLs updated successfully.")

except Exception as e:
    db.rollback()
    print(f"\nERROR: {e}")

finally:
    db.close()