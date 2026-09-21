from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class BaselineClassifier:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100_000,
            ngram_range=(1, 2),
            min_df=2,
        )

        self.model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
        )

    def fit(self, texts, labels):
        X = self.vectorizer.fit_transform(texts)

        self.model.fit(X, labels)

    def predict(self, texts):
        X = self.vectorizer.transform(texts)

        return self.model.predict(X)

    def predict_proba(self, texts):
        X = self.vectorizer.transform(texts)

        return self.model.predict_proba(X)

    