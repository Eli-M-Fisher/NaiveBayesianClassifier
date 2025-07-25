from core.data_loader import DataLoader
from model.naive_bayes import NaiveBayesClassifier
from inspector.dataset_inspector import DatasetInspector
from core.logger import logger
from core.cleaner import Cleaner
from core.trainer import Trainer
from core.validator import Validator
import pandas as pd


class Controller:
    def __init__(self, file_path: str, target_column: str):
        self.__file_path = file_path
        self.__target_column = target_column
        self._data_loader = DataLoader(file_path, target_column)
        self.__classifier = NaiveBayesClassifier()
        self.__inspector = DatasetInspector(file_path)
        self.__identifier_columns = self.__inspector.get_identifier_columns()

        # Extra manual logic for robustness:
        if "Index" not in self.__identifier_columns:
            self.__identifier_columns.append("Index")

        logger.info("Identifier columns used for cleaning: %s", self.__identifier_columns)

        self.__train_data = None
        self.__test_data = None
        self.__test_labels = None
        self.__analysis = None

        logger.info("Controller initialized for file: %s", file_path)

    def load_data(self):
        """
        Loads and splits the data into training and testing sets.
        Also performs dataset analysis using DatasetInspector.
        """
        try:
            self.__train_data, self.__test_data, self.__test_labels = self._data_loader.load_data()
            self.__analysis = self.__inspector.inspect()

            # Clean training data
            train_cleaner = Cleaner(self.__train_data)
            self.__train_data = train_cleaner.clean(self.__identifier_columns)

            # Clean test data
            test_cleaner = Cleaner(self.__test_data)
            self.__test_data = test_cleaner.clean(self.__identifier_columns)

            logger.info("Data loaded and preprocessed successfully.")
        except Exception as e:
            logger.error("Failed to load data: %s", str(e))
            raise

    def train(self):
        """
        Trains the classifier on the training dataset using Trainer module.
        """
        if self.__train_data is not None:
            logger.info("Preparing Trainer...")
            trainer = Trainer(self.__classifier)
            trainer.train(self.__train_data)
            print("[MODEL] Training completed.")
        else:
            logger.warning("No training data available.")
            print("[ERROR] No training data loaded.")

    def evaluate(self):
        """
        Evaluates the model on the test dataset using Validator module.
        """
        if self.__test_data is not None and self.__test_labels is not None:
            logger.info("Starting evaluation using Validator...")
            validator = Validator(self.__classifier)
            accuracy = validator.evaluate(self.__test_data, self.__test_labels)
            print(f"[EVALUATION] Accuracy on test set: {accuracy * 100:.2f}%")
        else:
            logger.warning("Test data not available.")
            print("[ERROR] Test data not available.")

    def classify_record(self, record: dict):
        """
        Legacy direct classification method.
        """
        logger.info("Classifying single record (legacy classify_record)...")
        return self.__classifier.classify_record(record)

    def predict_single(self, record: dict) -> str:
        """
        Classify a single record using the trained model.
        Ensures identifier columns (like 'Index') are removed first.
        """
        df = pd.DataFrame([record])

        logger.info("Input features for prediction: %s", df.columns.tolist())

        # Drop identifier columns safely
        df = df.drop(columns=self.__identifier_columns, errors="ignore")

        logger.info("Predicting single record via API after cleaning...")
        prediction = self.__classifier.predict(df)
        logger.info("Prediction result: %s", prediction[0])
        return str(prediction[0])

    def get_column_metadata(self):
        """
        Returns column metadata from the dataset inspector,
        excluding the target column.
        """
        metadata = self.__inspector.get_column_metadata()
        return {col: dtype for col, dtype in metadata.items() if col != self.__target_column}

    @property
    def dataset_analysis(self):
        return self.__analysis

    @property
    def identifier_columns(self):
        return self.__identifier_columns
