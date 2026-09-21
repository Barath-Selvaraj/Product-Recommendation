from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.core.exceptions import DatabaseException

class ProductRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, product: Product) -> Product:

        try:
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)

            return product

        except SQLAlchemyError as exc:
            self.db.rollback()

            raise DatabaseException() from exc

    def get_by_id(
        self,
        product_id: str,
        product_locale: str,
    ) -> Product | None:

        try:
            statement = select(Product).where(
                Product.product_id == product_id,
                Product.product_locale == product_locale,
            )

            return self.db.scalar(statement)

        except SQLAlchemyError as exc:
            raise DatabaseException() from exc

    def search_similar(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ):

        try:
            similarity = (
                1 - Product.embedding.cosine_distance(
                query_embedding
                )
            )

            statement = (
                select(
                    Product,
                    similarity.label("similarity"),
                )
                .where(Product.embedding.is_not(None))
                .order_by(
                    Product.embedding.cosine_distance(
                        query_embedding
                    )
                )
                .limit(limit)
            )

            return self.db.execute(statement).all()

        except SQLAlchemyError as exc:
            raise DatabaseException() from exc