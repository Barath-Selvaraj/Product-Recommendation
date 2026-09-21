import os
import pandas as pd


EXAMPLES_PATH = "data/raw/shopping_queries_dataset_examples.parquet"
PRODUCTS_PATH = "data/raw/shopping_queries_dataset_products.parquet"
SOURCES_PATH = "data/raw/shopping_queries_dataset_sources.csv"

OUTPUT_DIR = "data/processed/shopping_queries_us"


def prepare_us_dataset():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Loading examples...")
    examples = pd.read_parquet(EXAMPLES_PATH)

    print("Loading products...")
    products = pd.read_parquet(PRODUCTS_PATH)

    print("Loading sources...")
    sources = pd.read_csv(SOURCES_PATH)

    # US only
    examples = examples[
        examples["product_locale"] == "us"
    ].copy()

    products = products[
        products["product_locale"] == "us"
    ].copy()

    # Merge product information
    df = examples.merge(
        products,
        on=["product_id", "product_locale"],
        how="left",
        validate="many_to_one",
    )

    # Add source information
    df = df.merge(
        sources,
        on="query_id",
        how="left",
        validate="many_to_one",
    )

    # Preserve the dataset's original train/test split
    train = df[df["split"] == "train"].copy()
    test = df[df["split"] == "test"].copy()

    train.to_parquet(
        f"{OUTPUT_DIR}/train.parquet",
        index=False,
    )

    test.to_parquet(
        f"{OUTPUT_DIR}/test.parquet",
        index=False,
    )

    print("\nUS dataset prepared.")
    print("Total:", len(df))
    print("Train:", len(train))
    print("Test:", len(test))

    print("\nTrain labels:")
    print(train["esci_label"].value_counts())

    print("\nTest labels:")
    print(test["esci_label"].value_counts())


if __name__ == "__main__":
    prepare_us_dataset()