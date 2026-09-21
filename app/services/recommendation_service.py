from sqlalchemy.orm import Session

from app.ai.embedding_service import generate_embedding
from app.repositories.product_repository import ProductRepository
from app.services.esci_service import ESCIService


class RecommendationService:

    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.esci_service = ESCIService()

    def search_products(
        self,
        query: str,
        limit: int = 10,
    ):
        # 1. Convert query to embedding
        query_embedding = generate_embedding(query)
                                                                                                    
        # 2. Retrieve candidate products
        products = self.repository.search_similar(
            query_embedding=query_embedding,
            limit=limit,
        )

        # 3. Predict ESCI for candidates
        results = self.esci_service.predict(
            query=query,
            products=products,
        )

        return results