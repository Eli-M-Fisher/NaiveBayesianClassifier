class DynamicRecordInputHelper:
    def __init__(self, ignored_columns=None):
        self.ignored_columns = ignored_columns if ignored_columns else []

    def prompt_for_input(self, column_metadata: dict) -> dict:
        """
        Prompts the user to enter values for each feature dynamically.
        Returns a dictionary representing the record.
        Skips ignored columns and the target column.
        """
        print("\nEnter feature values:")
        record = {}

        for column_name, metadata in column_metadata.items():
            if column_name.lower() == "class" or column_name in self.ignored_columns:
                continue  # Skip the target or ignored columns

            dtype = metadata["dtype"]

            while True:
                value = input(f"{column_name} ({dtype}): ")
                if dtype in ("int64", "float64"):
                    try:
                        value = float(value) if "." in value else int(value)
                        break
                    except ValueError:
                        print("Invalid number. Please try again.")
                else:
                    value = value.strip()
                    break

            record[column_name] = value

        if self.ignored_columns:
            print(f"[INFO] Skipped input for identifier columns: {self.ignored_columns}")

        return record