import pandas as pd
from sklearn.model_selection import train_test_split

class DataLoader:
    def __init__(self, file_path: str):
        self.__file_path = file_path
        self.__df = None

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loads CSV file, cleans it if needed, and splits into train and test sets.
        Returns: (train_df, test_df)
        """
        try:
            self.__df = pd.read_csv(self.__file_path)
            print(f"[DATA] Loaded dataset with shape: {self.__df.shape}")
        except Exception as e:
            print(f"[ERROR] Could not load file: {e}")
            raise

        # Split into 70% train, 30% test (with stratification on target 'class' if needed)
        train_df, test_df = train_test_split(self.__df, test_size=0.3, random_state=42, stratify=self.__df['class'])

        print(f"[DATA] Training set: {train_df.shape}, Testing set: {test_df.shape}")
        return train_df, test_df