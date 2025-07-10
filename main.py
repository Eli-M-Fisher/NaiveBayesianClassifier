from ui.user_interface import UserInterface

def main():
    print("=== Naive Bayes Classifier (Generic Framework) ===")
    file_path = input("Enter path to CSV file: ").strip()
    target_column = input("Enter name of target column: ").strip()

    try:
        ui = UserInterface(file_path, target_column)
        ui.run()
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()