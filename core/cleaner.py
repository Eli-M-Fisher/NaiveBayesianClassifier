import pandas as pd
from core.logger import logger


class Cleaner:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def drop_identifier_columns(self, identifier_columns: list[str]) -> None:
        """
        Removes identifier columns (like IDs, names) if present.
        """
        logger.info("Dropping identifier columns: %s", identifier_columns)
        self.df.drop(columns=identifier_columns, inplace=True, errors='ignore')

    def fill_missing_values(self, fill_value: str = "unknown") -> None:
        """
        Fills missing values in the dataset with a default placeholder.
        """
        logger.info("Filling missing values with: '%s'", fill_value)
        self.df.fillna(fill_value, inplace=True)

    def convert_to_categorical(self) -> None:
        """
        Converts all columns to categorical data type (for Naive Bayes).
        """
        logger.info("Converting all columns to 'category' dtype.")
        for col in self.df.columns:
            self.df[col] = self.df[col].astype("category")

    def clean(self, identifier_columns: list[str] = None) -> pd.DataFrame:
        """
        Runs the full cleaning pipeline.
        """
        if identifier_columns:
            self.drop_identifier_columns(identifier_columns)

        self.fill_missing_values()
        self.convert_to_categorical()

        logger.info("Data cleaning completed. Resulting shape: %s", self.df.shape)
        return self.df
