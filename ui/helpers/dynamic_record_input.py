class DynamicRecordInputHelper:
    def __init__(self):
        pass  # No need to store metadata as a member

    def prompt_for_input(self, column_metadata: dict) -> dict:
        """
        Prompts the user to enter values for each feature dynamically.
        Returns a dictionary representing the record.
        """
        print("\nEnter feature values:")
        record = {}

        for column_name, metadata in column_metadata.items():
            if column_name == "class":
                continue  # Skip the target column

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

        return record