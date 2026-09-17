from PySide6.QtWidgets import QDialog,QVBoxLayout,QCheckBox,QPushButton
from utils.config import config_manager


class DebugDialog(QDialog):

    
    def __init__(self, parent=None): 
        super().__init__(parent) 

        self.setWindowTitle("Debug Setting")
        self.setFixedSize(300, 250)

        self.debug_layout = QVBoxLayout(self)

        debug_items =[
                    ("live view", "Live view"),
                    ("Level Line", "Level Line"),
                    ("binary", "Binary Image"),
                    ("contour", "Contour"),
                    ("roi", "ROI"),
                    ("find_pin", "Find Pin"),
                    ("image_health", "Image Health"),
                    ("subpixel_image", "subpixel_image"),
                    ("result", "Final Result"),
                    ]

        self.debug_checkbox = {}

        for key, text in debug_items:

            checkbox = QCheckBox(text)

            self.debug_checkbox[key] = checkbox

            self.debug_layout.addWidget(checkbox)

        self.debug_button_close = QPushButton("Close")
        self.debug_layout.addWidget(self.debug_button_close)

        for key, checkbox in self.debug_checkbox.items():
            checkbox.setChecked(config_manager.debug[key])

        self.debug_button_close.clicked.connect(self.debug_button_close_clicker)

    def debug_button_close_clicker(self):

        for key, checkbox in self.debug_checkbox.items():
            config_manager.debug[key] = checkbox.isChecked()

        config_manager.save_config()

        self.accept()

