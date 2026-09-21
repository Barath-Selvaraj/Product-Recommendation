from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    product_locale: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    product_title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product_bullet_point: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    product_brand: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    product_color: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True,
    )