from app.core.database import SessionLocal
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.ai.embedding_service import generate_product_embedding

db = SessionLocal()

try:
    repository = ProductRepository(db)

    product = Product(
    product_id="TEST003",
    product_locale="en",
    product_title="Wireless Bluetooth Headphones",
    product_description="Over-ear wireless headphones",
    product_brand="TestBrand",
    product_color="Black",
    )

    product.embedding = generate_product_embedding(
    product_title=product.product_title,
    product_brand=product.product_brand,
    product_color=product.product_color,
    product_description=product.product_description,
    )

    created_product = repository.create(product)

    print("Created:")
    print(created_product.product_id)
    print(created_product.product_locale)

    fetched_product = repository.get_by_id(
    product_id="TEST003",
    product_locale="en",
)

    print("\nFetched:")
    print(fetched_product.product_id)
    print(fetched_product.product_title)
    print("\nEmbedding dimension:")
    print(len(fetched_product.embedding))
finally:
    db.close()