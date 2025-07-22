import os
import pandas as pd
import numpy as np
import math
import joblib
from collections import defaultdict
from model.base_model import BaseModel


# Helpers for nested defaultdicts (compatible with joblib pickling)
def nested_defaultdict():
    return defaultdict(float)

def double_nested_defaultdict():
    return defaultdict(nested_defaultdict)


class NaiveBayesClassifier(BaseModel):
    def __init__(self):
        self.__class_priors = {}
        self.__feature_likelihoods = defaultdict(double_nested_defaultdict)
        self.__classes = []

    def train(self, df: pd.DataFrame):
        features = df.columns[:-1]
        target_col = df.columns[-1]
        self.__classes = df[target_col].unique()

        class_counts = df[target_col].value_counts()
        total = len(df)
        self.__class_priors = {
            cls: class_counts[cls] / total for cls in self.__classes
        }

        self.__feature_likelihoods = defaultdict(double_nested_defaultdict)

        for feature in features:
            for feature_val in df[feature].unique():
                for cls in self.__classes:
                    numerator = len(df[(df[feature] == feature_val) & (df[target_col] == cls)]) + 1
                    denominator = len(df[df[target_col] == cls]) + df[feature].nunique()
                    prob = numerator / denominator
                    self.__feature_likelihoods[feature][feature_val][cls] = prob

        print("[MODEL] Training complete.")

    def predict(self, X: pd.DataFrame) -> list:
        predictions = []

        missing_features = [f for f in self.__feature_likelihoods if f not in X.columns]
        if missing_features:
            raise ValueError(f"Missing features in input data: {missing_features}")

        for idx in X.index:
            log_probs = {}
            try:
                for cls in self.__class_priors:
                    log_prob = math.log(self.__class_priors[cls])
                    for feature in self.__feature_likelihoods:
                        value = X.at[idx, feature]
                        likelihoods_for_value = self.__feature_likelihoods[feature].get(value)
                        likelihood = likelihoods_for_value.get(cls, 1e-6) if likelihoods_for_value else 1e-6
                        log_prob += math.log(likelihood)
                    log_probs[cls] = log_prob
                predicted_class = max(log_probs, key=log_probs.get)
                predictions.append(predicted_class)
            except Exception as e:
                print(f"[PREDICT ERROR] Row {idx} failed: {e}")
                raise

        return predictions

    def classify_record(self, record: dict) -> int:
        df = pd.DataFrame([record])
        return self.predict(df)[0]

    def evaluate(self, test_df: pd.DataFrame, test_labels: pd.Series) -> float:
        predictions = self.predict(test_df)
        correct = sum(p == t for p, t in zip(predictions, test_labels))
        return correct / len(test_labels)

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        feature_likelihoods_dict = {
            feature: {
                value: dict(class_probs)
                for value, class_probs in value_dict.items()
            }
            for feature, value_dict in self.__feature_likelihoods.items()
        }

        joblib.dump({
            "class_priors": self.__class_priors,
            "feature_likelihoods": feature_likelihoods_dict,
            "classes": self.__classes
        }, filepath)

    def load(self, filepath: str):
        data = joblib.load(filepath)
        self.__class_priors = data["class_priors"]
        self.__classes = data["classes"]

        self.__feature_likelihoods = defaultdict(double_nested_defaultdict)
        for feature, value_dict in data["feature_likelihoods"].items():
            for value, class_probs in value_dict.items():
                for cls, prob in class_probs.items():
                    self.__feature_likelihoods[feature][value][cls] = prob
