import joblib

from ml.data.preprocessor import create_combined_text


MODEL_PATH = "artifacts/models/baseline_classifier.pkl"


class ESCIService:

    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, query: str, products):
        results = []

        for product, similarity in products:

            product_data = {
                "query": query,
                "product_title": product.product_title,
                "product_brand": product.product_brand,
                "product_color": product.product_color,
               "product_bullet_point": product.product_bullet_point,
                "product_description": product.product_description,
            }

            import pandas as pd

            df = pd.DataFrame([product_data])
            df = create_combined_text(df)

            text = df["combined_text"]

            prediction = self.model.predict(text)[0]
            probabilities = self.model.predict_proba(text)[0]
            classes = self.model.model.classes_

            probability_map = {
                cls: float(prob)
                for cls, prob in zip(classes, probabilities)
            }

            results.append({
                "product_id": product.product_id,
                "product_locale": product.product_locale,
                "product_title": product.product_title,
                "product_description": product.product_description,
                "product_bullet_point": product.product_bullet_point,
                "product_brand": product.product_brand,
                "product_color": product.product_color,

                "similarity_score": float(similarity),

                "esci_label": prediction,
                "probabilities": probability_map,
            })

        return results