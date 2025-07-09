from model.naive_bayes import NaiveBayesClassifier
from core.data_loader import DataLoader
from core.classifier_interface import ClassifierInterface

class Controller:
    def __init__(self, file_path: str, target_column: str):
        self.__file_path = file_path
        self.__target_column = target_column
        self.__classifier = NaiveBayesClassifier()
        self.__interface = ClassifierInterface(self.__classifier)
        self.__train_df = None
        self.__test_df = None
        self.__test_labels = None
        self.__feature_names = []

    def train_model(self):
        loader = DataLoader(self.__file_path, self.__target_column)
        self.__train_df, self.__test_df, self.__test_labels = loader.load_data()
        self.__classifier.train(self.__train_df)
        self.__feature_names = list(self.__train_df.columns[:-1])  # Save for user input
        print("[SYSTEM] Model training completed successfully.\n")

    def run_file_classification(self):
        if self.__test_df is None or self.__test_labels is None:
            print("[ERROR] Model must be trained before classification.\n")
            return

        accuracy = self.__interface.classify_file(self.__test_df, self.__test_labels)
        print(f"[RESULT] Final Accuracy: {accuracy:.2f}%\n")

    def run_single_classification(self, record: dict):
        result = self.__interface.classify_record(record)
        print(f"[RESULT] This record was classified as: {result}\n")

    def get_feature_names(self) -> list:
        return self.__feature_names