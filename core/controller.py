from core.data_loader import DataLoader
from model.naive_bayes import NaiveBayesClassifier
from inspector.dataset_inspector import DatasetInspector
import pandas as pd


class Controller:
    def __init__(self, file_path: str, target_column: str):
        self.__file_path = file_path
        self.__target_column = target_column
        self._data_loader = DataLoader(file_path, target_column)
        self.__classifier = NaiveBayesClassifier()
        self.__inspector = DatasetInspector(file_path)
        self.__identifier_columns = self.__inspector.get_identifier_columns()

        self.__train_data = None
        self.__test_data = None
        self.__test_labels = None
        self.__analysis = None

    def load_data(self):
        """
        Loads and splits the data into training and testing sets.
        Also performs dataset analysis using DatasetInspector.
        """
        self.__train_data, self.__test_data, self.__test_labels = self._data_loader.load_data()
        self.__inspector.inspect()

        if self.__identifier_columns:
            print(f"[INFO] Ignored identifier columns during training: {self.__identifier_columns}")
            self.__train_data = self.__train_data.drop(columns=self.__identifier_columns, errors="ignore")
            self.__test_data = self.__test_data.drop(columns=self.__identifier_columns, errors="ignore")

    def train(self):
        """
        Trains the classifier on the training dataset.
        """
        if self.__train_data is not None:
            self.__classifier.train(self.__train_data)
            print("[MODEL] Training completed.")
        else:
            print("[ERROR] No training data loaded.")

    def evaluate(self):
        """
        Evaluates the model on the test dataset.
        """
        if self.__test_data is not None and self.__test_labels is not None:
            accuracy = self.__classifier.evaluate(self.__test_data, self.__test_labels)
            print(f"[EVALUATION] Accuracy on test set: {accuracy * 100:.2f}%")
        else:
            print("[ERROR] Test data not available.")

    def classify_record(self, record: dict):
        """
        Classifies a single record using the trained classifier.
        """
        return self.__classifier.classify_record(record)

    def get_column_metadata(self):
        """
        Returns column metadata from the dataset inspector,
        excluding the target column.
        """
        metadata = self.__inspector.get_column_metadata()
        return {col: dtype for col, dtype in metadata.items() if col != self.__target_column}

    def predict_single(self, record: dict) -> str:
        """
        Classify a single record using the trained model.
        """
        if self.__classifier is None:
            raise ValueError("Model has not been initialized.")

        df = pd.DataFrame([record])

        # Drop identifier columns if they exist
        df = df.drop(columns=self.__identifier_columns, errors="ignore")

        prediction = self.__classifier.predict(df)
        return str(prediction[0])

    @property
    def dataset_analysis(self):
        return self.__analysis