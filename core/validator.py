from core.logger import logger
from sklearn.metrics import accuracy_score


class Validator:
    def __init__(self, model):
        """
        Initializes the validator with a predictive model.
        The model must have a `.predict(df)` method.
        """
        self.model = model

    def evaluate(self, test_data, true_labels) -> float:
        """
        Evaluates model predictions against true labels.
        Returns accuracy as float.
        """
        if test_data is None or true_labels is None:
            logger.error("Validation failed: Missing test data or labels.")
            raise ValueError("Test data and labels must be provided.")

        logger.info("Generating predictions for evaluation...")
        predictions = self.model.predict(test_data)
        accuracy = accuracy_score(true_labels, predictions)
        logger.info("Model accuracy: %.2f%%", accuracy * 100)
        return accuracy
