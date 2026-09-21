from app.ai.model_loader import load_embedding_model
from app.core.exceptions import EmbeddingGenerationException

model = load_embedding_model()


def generate_embedding(text: str):

    try:
        return model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()

    except Exception as exc:
        raise EmbeddingGenerationException() from exc


def generate_embeddings(texts: list[str]):
    return model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
    )


def create_product_text(
    product_title: str,
    product_brand: str = "",
    product_color: str = "",
    product_bullet_point: str = "",
    product_description: str = "",
):
    return " ".join([
        product_title,
        product_brand,
        product_color,
        product_bullet_point,
        product_description,
    ])


def generate_product_embedding(
    product_title: str,
    product_brand: str = "",
    product_color: str = "",
    product_bullet_point: str = "",
    product_description: str = "",
):
    product_text = create_product_text(
        product_title,
        product_brand,
        product_color,
        product_bullet_point,
        product_description,
    )

    return generate_embedding(product_text)