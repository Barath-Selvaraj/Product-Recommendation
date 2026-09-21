from app.core.database import SessionLocal
from app.services.recommendation_service import RecommendationService


db = SessionLocal()

try:
    service = RecommendationService(db)

    results = service.search_products(
        query="wireless headphones",
        limit=5,
    )

    print("\nRecommendations:")

    for product in results:
        print(
            product.product_id,
            "|",
            product.product_title,
        )

finally:
    db.close()