from ui.user_interface import UserInterface

def main():
    print("=== Naive Bayes Classifier (Generic Framework) ===")
    file_path = input("Enter path to CSV file: ").strip()
    target_column = input("Enter name of target column: ").strip()

    ui = UserInterface(file_path, target_column)
    ui.run()

if __name__ == "__main__":
    main()