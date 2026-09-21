import joblib
import pandas as pd

from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from ml.data.preprocessor import (
    fill_missing_text,
    create_combined_text,
)


TEST_PATH = "data/processed/shopping_queries_us/test.parquet"
MODEL_PATH = "artifacts/models/baseline_classifier.pkl"


def evaluate():

    print("Loading test data...")

    test_df = pd.read_parquet(TEST_PATH)

    print("Test rows:", len(test_df))

    # Handle missing text
    test_df = fill_missing_text(test_df)

    # Create query + product text
    test_df = create_combined_text(test_df)

    # Load trained model
    model = joblib.load(MODEL_PATH)

    print("Running predictions...")

    predictions = model.predict(
        test_df["combined_text"]
    )

    actual = test_df["esci_label"]

    print("\nAccuracy:")
    print(accuracy_score(actual, predictions))

    print("\nClassification Report:")
    print(
        classification_report(
            actual,
            predictions,
        )
    )
    
    cm = confusion_matrix(
        actual,
        predictions,
        labels=["E", "S", "C", "I"]
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["E", "S", "C", "I"]
    )

    disp.plot(values_format="d")
    plt.title("ESCI Confusion Matrix")
    plt.show()   


if __name__ == "__main__":
    evaluate()