from PySide6.QtWidgets import QVBoxLayout,QWidget,QPushButton
from PySide6.QtCore import Qt

from style.font_style_manager import FontStyle

font_size = 20
class LeftButtonPanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setObjectName("LeftButtonPanel") 
        self.setAutoFillBackground(True) 
        self.setAttribute(Qt.WA_StyledBackground, True) 
        self.setFixedWidth(250)

    def initialize(self):

        self.left_panel_button_layout = QVBoxLayout(self)

        self.start_button = QPushButton("Start") 
        self.start_button.setFont(FontStyle.arial_font(True,False,font_size))
        self.start_button.setObjectName("StartButton")
  
        
        self.stop_button = QPushButton("Stop") 
        self.stop_button.setFont(FontStyle.arial_font(True,False,font_size))
        self.stop_button.setObjectName("StopButton") 

        self.manual_button = QPushButton("Manual") 
        self.manual_button.setFont(FontStyle.arial_font(True,False,font_size))
        # self.manual_button.setObjectName("ManualButton") 


        self.auto_button = QPushButton("Auto") 
        self.auto_button.setFont(FontStyle.arial_font(True,False,font_size))
        # self.auto_button.setObjectName("AutoButton")


        self.uart_button = QPushButton("Uart") 
        self.uart_button.setFont(FontStyle.arial_font(True,False,font_size))
        # self.uart_button.setObjectName("UartButton")


        self.modbus_button = QPushButton("Modbus") 
        self.modbus_button.setFont(FontStyle.arial_font(True,False,font_size))
        # self.modbus_button.setObjectName("ModbusButton")


        self.buttons = { 
            "start": self.start_button,
            "stop": self.stop_button,
            "manual": self.manual_button,
            "auto": self.auto_button,
            "uart": self.uart_button,
            "modbus": self.modbus_button,
        }



        self.left_panel_button_layout.setContentsMargins(20, 30, 20, 30)
        self.left_panel_button_layout.setSpacing(40)
        self.left_panel_button_layout.addStretch() 
        self.left_panel_button_layout.addWidget(self.start_button)
        self.left_panel_button_layout.addWidget(self.stop_button)
        self.left_panel_button_layout.addWidget(self.manual_button)
        self.left_panel_button_layout.addWidget(self.auto_button)
        self.left_panel_button_layout.addWidget(self.uart_button)
        self.left_panel_button_layout.addWidget(self.modbus_button)
        self.left_panel_button_layout.addStretch()
