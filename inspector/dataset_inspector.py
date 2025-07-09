import pandas as pd
import numpy as np
import re


class DatasetInspector:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = None
        self.feature_info = {}
        self.target_column = None

    def inspect(self):
        print("[INSPECT] Loading dataset...")
        self.df = pd.read_csv(self.file_path)

        print(f"[INSPECT] Dataset shape: {self.df.shape}\n")
        print("[INSPECT] Column summary:")

        for column in self.df.columns:
            col_data = self.df[column]
            col_type = self._infer_column_type(col_data)
            self.feature_info[column] = col_type
            print(f"  - {column} ({col_type})")

        print()

    def set_target_column(self, column_name: str):
        if column_name not in self.df.columns:
            raise ValueError(f"[ERROR] Column '{column_name}' not found in dataset.")
        self.target_column = column_name
        print(f"[INSPECT] Target column set to: {self.target_column} ({self.feature_info[column_name]})\n")

    def get_feature_info(self):
        return {k: v for k, v in self.feature_info.items() if k != self.target_column}

    def get_target_info(self):
        return {
            "name": self.target_column,
            "type": self.feature_info.get(self.target_column)
        }

    def _infer_column_type(self, series: pd.Series):
        if series.dtype == object:
            sample = series.dropna().astype(str).sample(min(20, len(series)), random_state=1)
            if all(self._is_url(val) for val in sample):
                return "url"
            else:
                return "text"
        elif pd.api.types.is_numeric_dtype(series):
            unique_vals = series.dropna().unique()
            if set(unique_vals).issubset({0, 1}):
                return "binary"
            elif len(unique_vals) < 10:
                return "categorical"
            else:
                return "numeric"
        else:
            return "unknown"

    def _is_url(self, value: str):
        return re.match(r'^https?://', value) is not None