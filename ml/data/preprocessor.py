PRODUCT_TEXT_COLUMNS = [
    "product_title",
    "product_brand",
    "product_color",
    "product_bullet_point",
    "product_description",
]


def fill_missing_text(df):
    df = df.copy()

    for column in PRODUCT_TEXT_COLUMNS:
        df[column] = df[column].fillna("").astype(str)

    df["query"] = df["query"].fillna("").astype(str)

    return df


def create_combined_text(df):
    df = df.copy()

    df["combined_text"] = (
        df["query"] + " " +
        df["product_title"] + " " +
        df["product_brand"] + " " +
        df["product_color"] + " " +
        df["product_bullet_point"] + " " +
        df["product_description"]
    )

    return df