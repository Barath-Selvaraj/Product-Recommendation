from app.core.database import SessionLocal
from app.models.product import Product


db = SessionLocal()

try:
    deleted = db.query(Product).delete()
    db.commit()

    print(f"Deleted {deleted} products.")

finally:
    db.close()