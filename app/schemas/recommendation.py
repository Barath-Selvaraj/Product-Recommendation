from pydantic import BaseModel


class ESCIProbabilities(BaseModel):
    E: float
    S: float
    I: float
    C: float


class RecommendationResponse(BaseModel):
    product_id: str
    product_locale: str
    product_title: str | None = None
    product_description: str | None = None
    product_bullet_point: str | None = None
    product_brand: str | None = None
    product_color: str | None = None

    similarity_score: float
    
    esci_label: str
    probabilities: ESCIProbabilities