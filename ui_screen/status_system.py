from PySide6.QtWidgets import QVBoxLayout,QWidget,QGroupBox,QLabel
from style.font_style_manager import FontStyle

class SystemStatus(QWidget):

    def __init__(self,main_window):

        super().__init__()

        self.main_window = main_window
        self.setFixedSize(200,295)

    def initialize(self):
        self.system_status_layout = QVBoxLayout(self)

        # 1. QGroupBox 标题在边框线上
        self.status_box = QGroupBox("System Status")
        self.status_box.setFont(FontStyle.arial_font(True,False,14))
        self.status_box.setStyleSheet("""
            QGroupBox {
                color: white; 
                background-color: #1E1E1E; 
                border: 2px solid #0078FF; 
                border-radius: 5px; 
                margin-top: 15px; /* 标题要空间 */
            }
            QGroupBox::title {
                subcontrol-origin: margin; /* 标题在边框上 */
                subcontrol-position: top center; /* 居中 */
                padding: 2px 10px; /* 左右空隙 */
                background-color: #0078FF; /* 给你加上蓝底，跟截图一样 */
                color: white; 
                border-radius: 3px;
            }
        """)  

        # 2. 下面4行状态 用QLabel
        self.label_camera = QLabel("Camera : ")
        self.label_manual = QLabel("Manual : ")
        self.label_auto = QLabel("Auto : ")
        self.label_uart = QLabel("Uart : ")
        self.label_modbus = QLabel("Modbus : " )

    
        for label in [self.label_camera, self.label_manual, self.label_auto, self.label_uart,self.label_modbus]:
            label.setStyleSheet("color: #0078FF; font-size: 14px; font-weight: bold; background: transparent;")

        
        box_layout = QVBoxLayout() 
        box_layout.setContentsMargins(10, 10, 10, 10)
        box_layout.setSpacing(6)
        box_layout.addWidget(self.label_camera)
        box_layout.addWidget(self.label_manual)
        box_layout.addWidget(self.label_auto)
        box_layout.addWidget(self.label_uart)
        box_layout.addWidget(self.label_modbus)
        
        self.status_box.setLayout(box_layout) 

      
        self.system_status_layout.addWidget(self.status_box)
        
    def update_system_status(self, name, status):

        label = getattr(self, f"label_{name.lower()}") # camera
        label.setText(f"{name} : {status}")
        
        # color = "#0078FF" if status == "OK" else "red"

        if status == "OK":

            color = "red"
        else:  
            color = "#0078FF"  
        label.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
            