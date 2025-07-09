from core.data_loader import DataLoader
from core.classifier_interface import ClassifierInterface
from model.naive_bayes import NaiveBayesClassifier
from inspector.dataset_inspector import DatasetInspector


class Controller:
    def __init__(self):
        self.__data_loader = DataLoader()
        self.__classifier = NaiveBayesClassifier()
        self.__interface = ClassifierInterface(self.__classifier)
        self.__data = None
        self.__analysis = None

    def load_data(self, path: str, target_column: str):
        self.__data = self.__data_loader.load_data(path, target_column)
        self.__analysis = DatasetInspector(self.__data).analyze()
        return self.__data

    def train(self):
        if self.__data:
            self.__interface.train(self.__data)

    def evaluate(self):
        if self.__data:
            return self.__interface.evaluate(self.__data)

    def classify_record(self, record: dict):
        return self.__interface.classify_record(record)

    @property
    def dataset_analysis(self):
        return self.__analysis