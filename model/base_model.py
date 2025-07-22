from abc import ABC, abstractmethod
import pandas as pd


class BaseModel(ABC):
    """
    Abstract base class for all classification models.
    Defines the standard interface expected by the Trainer and Validator.
    """

    @abstractmethod
    def train(self, df: pd.DataFrame) -> None:
        """
        Trains the model on the provided DataFrame.
        The last column of the DataFrame is expected to be the target column.
        """
        pass

    @abstractmethod
    def predict(self, df: pd.DataFrame) -> list:
        """
        Predicts labels for the given input DataFrame.
        Returns a list of predicted classes.
        """
        pass

    @abstractmethod
    def classify_record(self, record: dict) -> int:
        """
        Predicts a single record provided as a dictionary.
        Returns the predicted class.
        """
        pass

    @abstractmethod
    def evaluate(self, test_df: pd.DataFrame, test_labels: pd.Series) -> float:
        """
        Evaluates the model's accuracy on the test set.
        """
        pass
