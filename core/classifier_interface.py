import pandas as pd
from model.naive_bayes import NaiveBayesClassifier

class ClassifierInterface:
    def __init__(self, classifier: NaiveBayesClassifier):
        self.__classifier = classifier

    def classify_file(self, test_df: pd.DataFrame, original_labels: pd.Series) -> float:
        """
        Classifies an entire test dataset and returns the accuracy.
        """
        predictions = self.__classifier.predict_batch(test_df)
        correct = sum(pred == true for pred, true in zip(predictions, original_labels))
        total = len(original_labels)
        accuracy = correct / total * 100
        print(f"[EVAL] Accuracy: {accuracy:.2f}% ({correct}/{total} correct)")
        return accuracy

    def classify_record(self, record: dict) -> int:
        """
        Classifies a single record and returns the predicted class.
        """
        prediction = self.__classifier.predict(record)
        print(f"[PREDICT] Predicted class: {prediction}")
        return prediction