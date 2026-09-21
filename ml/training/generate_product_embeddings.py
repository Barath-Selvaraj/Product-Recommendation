import pandas as pd
from sqlalchemy import text

from app.ai.embedding_service import (
    create_product_text,
    generate_embeddings,
)
from app.core.database import SessionLocal


CHUNK_SIZE = 500


def generate_embeddings_for_products():

    print("Loading products...")

    products = pd.read_parquet(
        "data/raw/shopping_queries_dataset_products.parquet"
    )

    print("Total products:", len(products))

    # --------------------------------------------------
    # 1. Keep only US products
    # --------------------------------------------------

    products = products[
        products["product_locale"] == "us"
    ].copy()

    print("US products:", len(products))

    # --------------------------------------------------
    # 2. Remove duplicate product_id + locale
    # --------------------------------------------------

    products = products.drop_duplicates(
        subset=["product_id", "product_locale"]
    )

    print("Unique US products:", len(products))

    # --------------------------------------------------
    # 3. Handle missing text values
    # --------------------------------------------------

    text_columns = [
        "product_title",
        "product_brand",
        "product_color",
        "product_bullet_point",
        "product_description",
    ]

    products[text_columns] = (
        products[text_columns]
        .fillna("")
        .astype(str)
    )

    # --------------------------------------------------
    # 4. Connect to PostgreSQL
    # --------------------------------------------------

    db = SessionLocal()

    try:

        # --------------------------------------------------
        # 5. Find products that already have embeddings
        # --------------------------------------------------

        print("\nChecking existing embeddings...")

        existing_ids = db.execute(
            text(
                """
                SELECT product_id
                FROM products
                WHERE product_locale = 'us'
                  AND embedding IS NOT NULL
                """
            )
        ).scalars().all()

        existing_ids = set(existing_ids)

        print(
            "Products already embedded:",
            len(existing_ids)
        )

        # --------------------------------------------------
        # 6. Remove already embedded products
        # --------------------------------------------------

        products = products[
            ~products["product_id"].isin(existing_ids)
        ].copy()

        print(
            "Products remaining:",
            len(products)
        )

        if len(products) == 0:

            print(
                "\nAll US products already have embeddings."
            )

            return

        # --------------------------------------------------
        # 7. Process products in chunks
        # --------------------------------------------------

        total = len(products)

        statement = text(
            """
            UPDATE products
            SET embedding = CAST(:embedding AS vector)
            WHERE product_id = :product_id
              AND product_locale = :product_locale
            """
        )

        for start in range(
            0,
            total,
            CHUNK_SIZE,
        ):

            end = min(
                start + CHUNK_SIZE,
                total,
            )

            chunk = products.iloc[
                start:end
            ].copy()

            print(
                f"\nProcessing products "
                f"{start + 1}-{end} / {total}"
            )

            # --------------------------------------------------
            # 8. Create product text
            # --------------------------------------------------

            product_texts = [
                create_product_text(
                    product_title=row["product_title"],
                    product_brand=row["product_brand"],
                    product_color=row["product_color"],
                    product_bullet_point=row[
                        "product_bullet_point"
                    ],
                    product_description=row[
                        "product_description"
                    ],
                )
                for _, row in chunk.iterrows()
            ]

            # --------------------------------------------------
            # 9. Generate embeddings
            # --------------------------------------------------

            print("Generating embeddings...")

            embeddings = generate_embeddings(
                product_texts
            )

            print(
                "Embedding shape:",
                embeddings.shape,
            )

            # --------------------------------------------------
            # 10. Save embeddings to PostgreSQL
            # --------------------------------------------------

            for (_, row), embedding in zip(
                chunk.iterrows(),
                embeddings,
            ):

                db.execute(
                    statement,
                    {
                        "product_id": row[
                            "product_id"
                        ],
                        "product_locale": row[
                            "product_locale"
                        ],
                        "embedding": str(
                            embedding.tolist()
                        ),
                    },
                )

            db.commit()

            print(
                "Chunk saved to PostgreSQL."
            )

            # --------------------------------------------------
            # 11. Progress
            # --------------------------------------------------

            processed = end

            percentage = (
                processed / total
            ) * 100

            print(
                f"Progress: "
                f"{processed}/{total} "
                f"({percentage:.2f}%)"
            )

        print(
            "\nAll remaining US product "
            "embeddings generated successfully."
        )

    except Exception:

        db.rollback()

        print(
            "\nERROR: Transaction rolled back."
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    generate_embeddings_for_products()