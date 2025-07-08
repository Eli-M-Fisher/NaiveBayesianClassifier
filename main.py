from core.controller import Controller
from ui.user_interface import UserInterface


def main():
    # Path to your phishing CSV dataset
    file_path = "data/phishing.csv"

    controller = Controller(file_path)
    ui = UserInterface(controller)
    ui.run()


if __name__ == "__main__":
    main()