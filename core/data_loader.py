import pandas as pd
from sklearn.model_selection import train_test_split

class DataLoader:
    def __init__(self, file_path: str, target_column: str):
        self.__file_path = file_path
        self.__target_column = target_column
        self.__df = None

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
        """
        Loads CSV file and splits into train and test sets.
        Returns: (train_df, test_df, test_labels)
        """
        try:
            self.__df = pd.read_csv(self.__file_path)
            print(f"[DATA] Loaded dataset with shape: {self.__df.shape}")
        except Exception as e:
            print(f"[ERROR] Could not load file: {e}")
            raise

        if self.__target_column not in self.__df.columns:
            raise ValueError(f"[ERROR] Target column '{self.__target_column}' not found in dataset.")

        # Split
        train_df, test_df = train_test_split(
            self.__df,
            test_size=0.3,
            random_state=42,
            stratify=self.__df[self.__target_column]
        )

        print(f"[DATA] Training set: {train_df.shape}, Testing set: {test_df.shape}")

        # Separate labels from test set
        test_labels = test_df[self.__target_column]
        test_df = test_df.drop(columns=[self.__target_column])

        return train_df, test_df, test_labels