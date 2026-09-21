import pandas as pd


def prepare_dataset():

    print("Loading raw datasets...")

    examples = pd.read_parquet(
        "data/raw/shopping_queries_dataset_examples.parquet"
    )

    products = pd.read_parquet(
        "data/raw/shopping_queries_dataset_products.parquet"
    )

    sources = pd.read_csv(
        "data/raw/shopping_queries_dataset_sources.csv"
    )

    print("Examples:", examples.shape)
    print("Products:", products.shape)
    print("Sources :", sources.shape)

    print("Merging examples + products...")

    df = examples.merge(
        products,
        on=["product_id", "product_locale"],
        how="left",
        validate="many_to_one",
    )

    print("After product merge:", df.shape)

    print("Merging sources...")

    df = df.merge(
        sources,
        on="query_id",
        how="left",
        validate="many_to_one",
    )

    print("Final dataset:", df.shape)

    # Split using the dataset's existing split column
    train_df = df[df["split"] == "train"].copy()
    test_df = df[df["split"] == "test"].copy()

    print("Train:", train_df.shape)
    print("Test :", test_df.shape)

    # Save processed datasets
    train_df.to_parquet(
        "data/processed/train.parquet",
        index=False,
    )

    test_df.to_parquet(
        "data/processed/test.parquet",
        index=False,
    )

    print("Processed datasets saved successfully.")


if __name__ == "__main__":
    prepare_dataset()