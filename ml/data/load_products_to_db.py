import pandas as pd

from app.core.database import SessionLocal
from app.models.product import Product


FILE_PATH = "data/raw/shopping_queries_dataset_products.parquet"
CHUNK_SIZE = 5000


def load_products():
    print("Loading product dataset...")

    df = pd.read_parquet(FILE_PATH)
    df = df[df["product_locale"] == "us"].copy()

    print("US products:", len(df))

    # Keep only one row for each product + locale
    df = df.drop_duplicates(
        subset=["product_id", "product_locale"]
    )

    print("Unique products:", len(df))

    columns = [
        "product_id",
        "product_locale",
        "product_title",
        "product_description",
        "product_bullet_point",
        "product_brand",
        "product_color",
    ]

    df = df[columns]

    db = SessionLocal()

    try:
        for start in range(0, len(df), CHUNK_SIZE):

            chunk = df.iloc[start:start + CHUNK_SIZE]

            products = [
                Product(
                    product_id=row["product_id"],
                    product_locale=row["product_locale"],
                    product_title=row["product_title"],
                    product_description=row["product_description"],
                    product_bullet_point=row["product_bullet_point"],
                    product_brand=row["product_brand"],
                    product_color=row["product_color"],
                )
                for _, row in chunk.iterrows()
            ]

            db.bulk_save_objects(products)
            db.commit()

            print(
                f"Inserted {min(start + CHUNK_SIZE, len(df))}"
                f" / {len(df)}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    load_products()