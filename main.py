import sys
from PySide6.QtWidgets import QApplication
from ui_screen.main_ui import MyMainPage


def main():
    app = QApplication(sys.argv)

    window = MyMainPage()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
