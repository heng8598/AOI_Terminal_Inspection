from PySide6.QtGui import QFont

class FontStyle:

    @staticmethod
    def arial_font(bold, italic, size):

        font = QFont("Arial", size)
        font.setBold(bold)
        font.setItalic(italic)

        return font
    