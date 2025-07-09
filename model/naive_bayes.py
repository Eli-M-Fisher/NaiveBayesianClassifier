import pandas as pd
import numpy as np
import math
from collections import defaultdict


class NaiveBayesClassifier:
    def __init__(self):
        self.__class_priors = {}  # Prior probabilities for each class
        self.__feature_likelihoods = {}  # Nested dict: {feature: {value: {class: prob}}}
        self.__classes = []

    def train(self, df: pd.DataFrame):
        """
        Build the model from the training dataset using Laplace smoothing.
        Assumes the last column is the target.
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

    def predict(self, X: pd.DataFrame) -> list:
        """
        Predict classes for each row in a DataFrame.
        """
        predictions = []

        for idx in X.index:
            log_probs = {}

            for cls in self.__class_priors:
                # Start with log prior
                log_prob = math.log(self.__class_priors[cls])

                for feature in self.__feature_likelihoods:
                    value = X.at[idx, feature]

                    likelihoods_for_value = self.__feature_likelihoods[feature].get(value)
                    if likelihoods_for_value is None:
                        likelihood = 1e-6  # Unknown value smoothing
                    else:
                        likelihood = likelihoods_for_value.get(cls, 1e-6)

                    log_prob += math.log(likelihood)

                log_probs[cls] = log_prob

            predicted_class = max(log_probs, key=log_probs.get)
            predictions.append(predicted_class)

        return predictions

    def classify_record(self, record: dict) -> int:
        """
        Predict a single record by wrapping it in a DataFrame.
        """
        df = pd.DataFrame([record])
        return self.predict(df)[0]

    def evaluate(self, test_df: pd.DataFrame, test_labels: pd.Series) -> float:
        """
        Evaluate the model by comparing predictions to the true labels.
        Returns accuracy as a float between 0 and 1.
        """
        predictions = self.predict(test_df)
        correct = sum(p == t for p, t in zip(predictions, test_labels))
        accuracy = correct / len(test_labels)
        return accuracy