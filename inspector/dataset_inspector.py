import pandas as pd
from typing import List, Dict


class DatasetInspector:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.identifier_columns = self._identify_identifier_columns()

    def inspect(self) -> Dict:
        """Return high-level info about dataset."""
        return {
            "shape": self.df.shape,
            "columns": self.df.columns.tolist(),
            "null_values": self.df.isnull().sum().to_dict(),
            "ignored_columns": self.identifier_columns
        }

    def extract_metadata(self) -> List[Dict[str, str]]:
        """Extract metadata about each feature: name and type."""
        metadata = []
        for column in self.df.columns:
            dtype = str(self.df[column].dtype)
            if dtype.startswith("int") or dtype.startswith("float"):
                col_type = "numeric"
            else:
                col_type = "categorical"
            metadata.append({"name": column, "type": col_type})
        return metadata

    def get_column_metadata(self) -> Dict[str, Dict[str, object]]:
        """
        Returns a dictionary with metadata about each column.
        Includes type, number of unique values, and missing values.
        """
        metadata = {}
        for column in self.df.columns:
            metadata[column] = {
                "dtype": self.df[column].dtype.name,
                "unique_values": self.df[column].nunique(),
                "missing_values": self.df[column].isnull().sum()
            }
        return metadata

    def _identify_identifier_columns(self) -> List[str]:
        """
        Heuristically identifies columns that likely represent identifiers,
        such as 'index', 'id', or unnamed columns.
        """
        identifier_cols = []
        for column in self.df.columns:
            name = column.strip().lower()
            if name == 'index' or name.endswith('_id') or name == 'id' or name.startswith('unnamed'):
                identifier_cols.append(column)
        return identifier_cols

    def get_identifier_columns(self) -> List[str]:
        return self.identifier_columns