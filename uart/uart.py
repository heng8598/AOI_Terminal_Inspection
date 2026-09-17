from PySide6.QtWidgets import QDialog,QVBoxLayout,QPushButton,QLabel,QComboBox,QLabel,QHBoxLayout,QVBoxLayout,QMessageBox
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from style.font_style_manager import FontStyle
from style.app_style_manager import AppStyle

import serial
import serial.tools.list_ports 


from utils.config import config_manager

class UARTDialog(QDialog):

    
    def __init__(self,main_window):

        super().__init__()
        self.main_window = main_window
        self.uart_app = AppStyle()
     

        model_mode = config_manager.comm_mode


        uart_baud = config_manager.uart["baudrate"]
        comm_port = config_manager.uart["com_port"]

        self.main_layout = QVBoxLayout()
        self.select_buadarate_layout = QHBoxLayout()
        self.comm_port_layout = QHBoxLayout()
        self.uart_save_layout = QHBoxLayout()
        self.uart_status_layout = QHBoxLayout()

        self.setWindowTitle("Uart Setting")
        self.setFixedSize(640, 480)
        self.uart_box, self.uart_group = \
        self.uart_app.create_dual_radio("Disable","Activate","UART SETUP",0,1)
        self.uart_box.setFixedHeight(50)

        self.select_baudrate = QLabel("Select Baudrate :")
        self.select_baudrate.setFont(FontStyle.arial_font(True,False,12))

        self.baudrate_box = QComboBox()
        self.baudrate_box.addItem("9600")
        self.baudrate_box.addItem("115200")

        self.comm_port = QLabel("Comm Port :")
        self.comm_port.setFont(FontStyle.arial_font(True,False,12))

        self.comm_port_box = QComboBox()
     
   
        self.uart_refresh_btn = QPushButton("Refresh")
        self.uart_refresh_btn.setFixedSize(120, 40)
        self.uart_refresh_btn.setIcon(QIcon("icons/refresh.svg"))
        self.uart_refresh_btn.setIconSize(QSize(20, 20))


        self.uart_save_btn = QPushButton("Save")
        self.uart_save_btn.setFixedSize(120, 40)
        self.uart_save_btn.setIcon(QIcon("icons/save.svg"))
        self.uart_save_btn.setIconSize(QSize(20, 20))

        self.uart_cancel_btn = QPushButton("Cancel")
        self.uart_cancel_btn.setFixedSize(120, 40)
        self.uart_cancel_btn.setIcon(QIcon("icons/cancel.svg"))
        self.uart_cancel_btn.setIconSize(QSize(20, 20))

  

        self.uart_save_layout.addStretch()
        self.uart_save_layout.addWidget(self.uart_refresh_btn)
        self.uart_save_layout.addWidget(self.uart_save_btn)
        self.uart_save_layout.addWidget(self.uart_cancel_btn)

        self.select_buadarate_layout.addWidget(self.select_baudrate)
        self.select_buadarate_layout.addWidget(self.baudrate_box)
      
       

        self.comm_port_layout.addWidget(self.comm_port) 
        self.comm_port_layout.addWidget(self.comm_port_box) 

        self.main_layout.addWidget(self.uart_box)
        self.main_layout.addLayout(self.select_buadarate_layout)
        self.main_layout.addLayout(self.comm_port_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.uart_status_layout)
        self.main_layout.addLayout(self.uart_save_layout)

        if model_mode["uart"] == 0:
            self.uart_group.button(0).setChecked(True)
            self.select_baudrate.setVisible(False)
            self.baudrate_box.setVisible(False)
            self.comm_port.setVisible(False)
            self.comm_port_box.setVisible(False)

        if model_mode["uart"] == 1:

            self.uart_group.button(1).setChecked(True)
            self.comm_port_box.addItem(str(comm_port))

        self.setLayout(self.main_layout)
       
        self.uart_group.buttonClicked.connect(self.on_radio_changer)
        self.uart_refresh_btn.clicked.connect(self.uart_refresh_btn_clicked)
        self.uart_cancel_btn.clicked.connect(self.uart_cancel_btn_clicked)
        self.uart_save_btn.clicked.connect(self.uart_save_btn_clicked)


    def on_radio_changer(self,button):

        button = self.uart_group.checkedId()
        
        if button == 0:
            self.uart_group.button(0).setChecked(True)

            self.select_baudrate.setVisible(False)
            self.baudrate_box.setVisible(False)
            self.comm_port.setVisible(False)
            self.comm_port_box.setVisible(False)
        

        elif button == 1:
            self.uart_group.button(1).setChecked(True)

            self.select_baudrate.setVisible(True)
            self.baudrate_box.setVisible(True)
            self.comm_port.setVisible(True)
            self.comm_port_box.setVisible(True)

    def uart_cancel_btn_clicked(self):

        self.reject()

    def uart_save_btn_clicked(self):

        uart_enable = self.uart_group.checkedId()
        baudrate = int(self.baudrate_box.currentText())
        com_port = self.comm_port_box.currentData()

        config_manager.comm_mode["uart"] = uart_enable
        config_manager.uart["baudrate"] = baudrate
        config_manager.uart["com_port"] = com_port

        config_manager.save_config()

        self.accept()

    def uart_refresh_btn_clicked(self):

        self.comm_port_box.clear()
        
        ports = serial.tools.list_ports.comports()
        for port in ports:
            text = f"{port.device} - {port.description}" 
            self.comm_port_box.addItem(text, port.device)

       
    
          
