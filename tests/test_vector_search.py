from app.core.database import SessionLocal
from app.ai.embedding_service import generate_embedding
from app.repositories.product_repository import ProductRepository


db = SessionLocal()

try:
    repository = ProductRepository(db)

    query = "wireless headphones"

    query_embedding = generate_embedding(query)

    results = repository.search_similar(
        query_embedding=query_embedding,
        limit=5,
    )

    print("\nSearch query:")
    print(query)

    print("\nSimilar products:")

    for product in results:
        print(
            product.product_id,
            "|",
            product.product_title,
        )

finally:
    db.close()