from PySide6.QtWidgets import QDialog,QLabel, QHBoxLayout,QLineEdit,QVBoxLayout,QGroupBox,QDialogButtonBox,\
                            QButtonGroup
from PySide6.QtCore import Qt

from style.font_style_manager import FontStyle
from camera.signal_bus import signal_bus
from utils.config import config_manager


class Calibration(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Calibration")
        self.setFixedSize(450, 250)

        self.notice_layout = QVBoxLayout()
        self.button_layout =QHBoxLayout()
        self.diamesion_layout = QVBoxLayout()

        self.pixel_widht_result = None

        self.notice = QLabel(
                "Calibration Procedure\n\n"
                "1. Please enable camera first\n"
                "2. Press the inspetion button to perform one inspection.\n"
                "3. Measure the Ground terminal width with a caliper.\n"
                "4. Enter the actual measured value (mm)."
            )
        self.notice.setFont(FontStyle.arial_font(True,False, 12))
        self.notice.setStyleSheet("color : blue")

        self.diamesion = QLineEdit()
        self.diamesion.setFixedSize(100,30)

        self.msg_diamesion = QLabel("Please In Value (mm)")
        self.msg_diamesion.setFont(FontStyle.arial_font(True,False, 10))

        self.pixel_widht_ground = QLabel("__")
        
        self.diamesion_layout.addWidget(self.diamesion, alignment=Qt.AlignCenter)
        self.diamesion_layout.addWidget(self.pixel_widht_ground , alignment=Qt.AlignCenter)
        self.diamesion_layout.addWidget(self.msg_diamesion, alignment=Qt.AlignCenter)
        



        self.button_box = QDialogButtonBox()

        # Save Cancel 按钮
        self.button_box.addButton(QDialogButtonBox.Save)
        self.button_box.addButton(QDialogButtonBox.Cancel)
        self.btn_inspect = self.button_box.addButton("▶ Inspection", QDialogButtonBox.ActionRole)
        self.btn_inspect.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")

        # 连接
        self.btn_inspect.clicked.connect(self.request_inspection)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.close)

        self.button_layout.addWidget(self.button_box)

        self.notice_layout.addWidget(self.notice)
        self.notice_layout.addLayout(self.diamesion_layout)
        self.notice_layout.addStretch()
        self.notice_layout.addWidget(self.button_box)

        signal_bus.inspection_result.connect(self.on_inspection_result)
     

        self.setLayout(self.notice_layout)

    def request_inspection(self):
        
        self.btn_inspect.setEnabled(False)
        self.btn_inspect.setText("⏳ Inspecting...")
        signal_bus.inspection_request.emit()

    def on_inspection_result(self,result):

        self.btn_inspect.setEnabled(True)
        self.btn_inspect.setText("▶ Inspect")

        data = result
        result_data = data.get("result")
   
        for item in result_data:

            if item["name"] == "ground":
                self.pixel_widht_result = item["width_termianl"]["width_pixel"]
                pixel_widht = f"{self.pixel_widht_result :.2f} Pixel "
                self.pixel_widht_ground.setText(pixel_widht)
                return
                


    def save_button_clicked(self):

        if self.pixel_widht_result is None:
            signal_bus.calibration_error.emit("Please inspect first.")
            return

        if not self.diamesion.text().strip():
            signal_bus.calibration_error.emit("Please enter width.")
            return

        # 2. 有数据才保存
        try:

            GROUND_TERMINAL_WIDTH = float(self.diamesion.text())

            GROUND_PIN_THICKNESS = 0.37
            # GROUND_PIN_THICKNESS = 0

            config_manager.calibration["width_mm"] = round((GROUND_TERMINAL_WIDTH - GROUND_PIN_THICKNESS),2)

            config_manager.calibration["width_pixel"] = round(float(self.pixel_widht_result),4)

            config_manager.save_config()
            self.accept() # 关闭窗口

        except ValueError:
            signal_bus.calibration_error.emit("Please enter a valid number in mm")


    def closeEvent(self, event):

        try:
            self.btn_inspect.setEnabled(True)
            self.btn_inspect.setText("▶ Inspect")
            signal_bus.inspection_result.disconnect(self.on_inspection_result)
        except Exception:
            pass

        super().closeEvent(event)    