from core.controller import Controller

class UserInterface:
    def __init__(self):
        self.__controller = None

    def run(self):
        print("=== Naive Bayes Classifier (Generic Framework) ===")
        file_path = input("Enter path to CSV file: ")
        target_column = input("Enter name of target column: ")

        try:
            self.__controller = Controller(file_path, target_column)
        except Exception as e:
            print(f"[ERROR] Failed to initialize controller: {e}")
            return

        while True:
            print("\n--- Menu ---")
            print("1. Train model")
            print("2. Classify full test set")
            print("3. Classify single record")
            print("4. Exit")
            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.__controller.train_model()

            elif choice == "2":
                self.__controller.run_file_classification()

            elif choice == "3":
                feature_names = self.__controller.get_feature_names()
                record = {}
                print("Enter feature values:")

                for name in feature_names:
                    value = input(f"  {name}: ")
                    try:
                        record[name] = int(value)
                    except ValueError:
                        print(f"[WARNING] Invalid input for {name}. Defaulting to 0.")
                        record[name] = 0

                self.__controller.run_single_classification(record)

            elif choice == "4":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please try again.")