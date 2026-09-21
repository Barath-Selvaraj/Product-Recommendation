from pydantic import BaseModel


class ProductResponse(BaseModel):
    product_id: str
    product_locale: str
    product_title: str | None = None
    product_description: str | None = None
    product_bullet_point: str | None = None
    product_brand: str | None = None
    product_color: str | None = None

    model_config = {
        "from_attributes": True
    }