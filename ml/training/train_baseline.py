import pandas as pd
import joblib

from ml.data.preprocessor import (
    fill_missing_text,
    create_combined_text,
)
from ml.models.baseline_classifier import BaselineClassifier


def train():

    print("Loading training data...")

    train_df = pd.read_parquet(
        "data/processed/shopping_queries_us/train.parquet"
    )

    print("Training rows:", len(train_df))

    # Handle missing text
    train_df = fill_missing_text(train_df)

    # Create query + product text
    train_df = create_combined_text(train_df)

    print("Rows used for training:", len(train_df))

    # Create classifier
    model = BaselineClassifier()

    print("Training model...")

    model.fit(
        train_df["combined_text"],
        train_df["esci_label"],
    )

    print("Training completed.")

    # Save trained model
    joblib.dump(
        model,
        "artifacts/models/baseline_classifier.pkl",
    )

    print("Model saved successfully.")

    return model


if __name__ == "__main__":
    train()