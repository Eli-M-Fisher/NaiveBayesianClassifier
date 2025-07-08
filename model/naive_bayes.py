import pandas as pd
import numpy as np
from collections import defaultdict

class NaiveBayesClassifier:
    def __init__(self):
        self.__class_priors = {}  # Prior probabilities for each class
        self.__feature_likelihoods = {}  # Nested dict: {feature: {value: {class: prob}}}
        self.__classes = []

    def train(self, df: pd.DataFrame):
        """
        Build the model from the training dataset using Laplace smoothing.
        """
        features = df.columns[:-1]
        target_col = df.columns[-1]
        self.__classes = df[target_col].unique()

        # Calculate prior probabilities
        class_counts = df[target_col].value_counts()
        total = len(df)
        self.__class_priors = {
            cls: class_counts[cls] / total for cls in self.__classes
        }

        # Initialize feature likelihoods with Laplace smoothing
        self.__feature_likelihoods = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        for feature in features:
            for feature_val in df[feature].unique():
                for cls in self.__classes:
                    numerator = len(df[(df[feature] == feature_val) & (df[target_col] == cls)]) + 1
                    denominator = len(df[df[target_col] == cls]) + df[feature].nunique()
                    prob = numerator / denominator
                    self.__feature_likelihoods[feature][feature_val][cls] = prob

        print("[MODEL] Training complete.")

    def predict(self, record: dict) -> int:
        """
        Predict the class of a single record (dictionary of feature_name -> value)
        """
        class_probs = {}

        for cls in self.__classes:
            prob = self.__class_priors[cls]
            for feature, value in record.items():
                likelihood = self.__feature_likelihoods[feature].get(value, {}).get(cls)
                if likelihood is None:
                    # Unknown value, apply uniform smoothing
                    likelihood = 1 / (sum(self.__class_priors.values()) + 1)
                prob *= likelihood
            class_probs[cls] = prob

        # Return the class with the highest posterior probability
        return max(class_probs, key=class_probs.get)

    def predict_batch(self, df: pd.DataFrame) -> list:
        """
        Predict classes for a DataFrame of records (no target column).
        """
        predictions = []
        for _, row in df.iterrows():
            record = row.to_dict()
            prediction = self.predict(record)
            predictions.append(prediction)
        return predictions