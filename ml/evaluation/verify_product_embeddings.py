import numpy as np
import pandas as pd


def verify_embeddings():

    embeddings = np.load(
        "artifacts/models/product_embeddings/embeddings_0001.npy"
    )

    metadata = pd.read_parquet(
        "artifacts/models/product_embeddings/metadata_0001.parquet"
    )

    print("Embeddings shape:", embeddings.shape)
    print("Metadata shape:", metadata.shape)

    print("\nFirst product:")
    print(metadata.iloc[0])

    print("\nFirst embedding:")
    print(embeddings[0][:10])

    assert len(embeddings) == len(metadata)
    assert embeddings.shape[1] == 384

    print("\nVerification successful.")


if __name__ == "__main__":
    verify_embeddings()