from core.controller import Controller
from ui.helpers.dynamic_record_input import DynamicRecordInputHelper


class UserInterface:
    def __init__(self):
        self.controller = Controller()

    def run(self):
        print("=== Naive Bayes Classifier (Generic Framework) ===")
        csv_path = input("Enter path to CSV file: ").strip()
        target_column = input("Enter name of target column: ").strip()
        self.controller.load_data(csv_path, target_column)

        while True:
            print("\n--- Menu ---")
            print("1. Train model")
            print("2. Classify full test set")
            print("3. Classify single record")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                self.controller.train()
            elif choice == "2":
                self.controller.evaluate()
            elif choice == "3":
                metadata = self.controller.get_column_metadata()
                input_helper = DynamicRecordInputHelper(metadata)
                record = input_helper.prompt_for_input()
                prediction = self.controller.predict_single(record)
                print(f"[PREDICTION] This record was classified as: {prediction}")
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")