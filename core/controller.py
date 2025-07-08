from model.naive_bayes import NaiveBayesClassifier
from core.data_loader import DataLoader
from core.classifier_interface import ClassifierInterface
from feature_extraction.url_feature_extractor import URLFeatureExtractor

class Controller:
    def __init__(self, file_path: str):
        self.__data_loader = DataLoader(file_path)
        self.__classifier = NaiveBayesClassifier()
        self.__interface = ClassifierInterface(self.__classifier)
        self.__train_df = None
        self.__test_df = None
        self.__test_labels = None

    def train_model(self):
        self.__train_df, full_test = self.__data_loader.load_data()
        self.__test_labels = full_test['class']
        self.__test_df = full_test.drop(columns=['class'])
        self.__classifier.train(self.__train_df)
        print("[SYSTEM] Model training completed successfully.\n")

    def run_file_classification(self):
        if self.__test_df is None or self.__test_labels is None:
            print("[ERROR] No test data available.")
            return
        accuracy = self.__interface.classify_file(self.__test_df, self.__test_labels)
        print(f"[RESULT] Final Accuracy: {accuracy:.2f}%\n")

    def run_single_classification(self, record: dict):
        result = self.__interface.classify_record(record)
        print(f"[RESULT] This record was classified as: {result}\n")

    def run_url_classification(self, url: str):
        if self.__classifier is None or not self.__classifier._NaiveBayesClassifier__class_priors:
            print("[ERROR] Model must be trained before classifying a URL.\n")
            return

        extractor = URLFeatureExtractor()
        features = extractor.extract(url)
        result = self.__interface.classify_record(features)
        print(f"[RESULT] The URL was classified as: {result}\n")