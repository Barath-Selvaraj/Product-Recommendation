from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.product import ProductResponse
from app.services.recommendation_service import RecommendationService
from app.schemas.recommendation import RecommendationResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("/", response_model=list[RecommendationResponse])
def get_recommendations(
    query: str,
    limit: int = 5,
    db: Session = Depends(get_db),
):
    service = RecommendationService(db)

    products = service.search_products(
        query=query,
        limit=limit,
    )

    return products