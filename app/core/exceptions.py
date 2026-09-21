class AppException(Exception):
    """
    Base exception for application-specific errors.
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)


class ProductNotFoundException(AppException):

    def __init__(self, product_id: str, product_locale: str):
        super().__init__(
            message=(
                f"Product '{product_id}' "
                f"with locale '{product_locale}' was not found."
            ),
            error_code="PRODUCT_NOT_FOUND",
            status_code=404,
        )


class RecommendationNotFoundException(AppException):

    def __init__(self):
        super().__init__(
            message="No Product Available",
            error_code="NO_PRODUCT_AVAILABLE",
            status_code=404,
        )


class EmbeddingGenerationException(AppException):

    def __init__(self):
        super().__init__(
            message="Failed to generate text embedding.",
            error_code="EMBEDDING_GENERATION_ERROR",
            status_code=500,
        )


class DatabaseException(AppException):

    def __init__(self):
        super().__init__(
            message="A database error occurred.",
            error_code="DATABASE_ERROR",
            status_code=500,
        )