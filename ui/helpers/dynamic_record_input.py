class DynamicRecordInputHelper:
    def __init__(self, column_metadata: list[dict]):
        self.column_metadata = column_metadata

    def prompt_for_input(self) -> dict:
        record = {}
        print("\nEnter feature values:")
        for column in self.column_metadata:
            name = column["column_name"]
            dtype = column["inferred_type"]
            suggestions = column["suggested_values"]

            while True:
                prompt = f"  {name}"
                if suggestions:
                    prompt += f" (e.g., {', '.join(map(str, suggestions[:3]))})"
                prompt += f" [{dtype}]: "

                user_input = input(prompt).strip()

                # Try to cast to appropriate type
                if dtype == "int":
                    try:
                        record[name] = int(user_input)
                        break
                    except ValueError:
                        print("    Please enter a valid integer.")
                elif dtype == "float":
                    try:
                        record[name] = float(user_input)
                        break
                    except ValueError:
                        print("    Please enter a valid number.")
                elif dtype == "bool":
                    if user_input.lower() in ("true", "false"):
                        record[name] = user_input.lower() == "true"
                        break
                    else:
                        print("    Please enter 'true' or 'false'.")
                else:
                    record[name] = user_input
                    break
        return record