import pandas as pd


def load_examples(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_products(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)


def load_sources(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

