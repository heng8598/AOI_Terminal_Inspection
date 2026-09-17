from PySide6.QtWidgets import QDialog, QLineEdit,QVBoxLayout,QLabel,QPushButton,QHBoxLayout,QMessageBox,QPlainTextEdit
from style.app_style_manager import AppStyle
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from utils.config import config_manager
from style.font_style_manager import FontStyle
from style.css_style import MyCSS

from connecting.modbus_connecting_manager import modbus_connecting_manager

class ModbusTCPDialog(QDialog):

    def __init__(self,main_window):
    
        super().__init__()
        self.main_window = main_window
        self.modbus_app = AppStyle() 
        self.link_mode_app = AppStyle() 

        model_mode = config_manager.comm_mode

        self.ip_address = config_manager.modbus_tcp["ip_address"]
        self.port = config_manager.modbus_tcp["port"]
        self.link_mode = config_manager.modbus_tcp["link_mode"]
        self.slave_id = config_manager.modbus_tcp["slave_id"]
        self.inspection_start = config_manager.modbus_tcp["inspection_start"]
        self.product_leave = config_manager.modbus_tcp["product_leave"]

        self.main_layout = QVBoxLayout()
        self.ip_layout = QHBoxLayout()
        self.port_layout = QHBoxLayout()
        self.slave_layout = QHBoxLayout()
        self.link_time_layout = QHBoxLayout()
        self.status_layout = QHBoxLayout()
        self.save_layout = QHBoxLayout()
        self.timer_start_layout = QHBoxLayout()
        self.timer_leave_layout = QHBoxLayout()
        self.notice_timer_layout = QVBoxLayout()



        self.setWindowTitle("Modbus TCP Setting")
        self.setFixedSize(640, 640)

        self.modbus_box, self.modbus_group = \
        self.modbus_app.create_dual_radio("Disable", "Activate", "MODBUS TCP SETUP", 0, 1)
        self.modbus_box.setFixedHeight(50)

        self.ip_label = QLabel("IP Address :")
        self.ip_label.setFont(FontStyle.arial_font(True, False, 12))
        self.ip_input = QLineEdit()
        self.ip_input.setFixedWidth(250)
        self.ip_input.setText(self.ip_address)

        self.port_label = QLabel("Port :")
        self.port_label.setFont(FontStyle.arial_font(True, False, 12))
        self.port_input = QLineEdit()
        self.port_input.setFixedWidth(250)
        self.port_input.setText(str(self.port))

        self.slave_label = QLabel("Slave ID :")
        self.slave_label.setFont(FontStyle.arial_font(True, False, 12))
        self.slave_input = QLineEdit()
        self.slave_input.setFixedWidth(250)
        self.slave_input.setText(str(self.slave_id))

        self.inspection_timer_label = QLabel("Inspection Timer Start M/s:")
        self.inspection_timer_label.setFont(FontStyle.arial_font(True, False, 12))
        self.inspection_timer_input = QLineEdit()
        self.inspection_timer_input.setFixedWidth(250)
        self.inspection_timer_input.setText(str(self.inspection_start))

        self.product_leave_label = QLabel("Product Leave Relay M/s:")
        self.product_leave_label.setFont(FontStyle.arial_font(True, False, 12))
        self.product_leave_input = QLineEdit()
        self.product_leave_input.setFixedWidth(250)
        self.product_leave_input.setText(str(self.product_leave))


        self.link_mode_box, self.link_mode_group = \
        self.link_mode_app.create_dual_radio("Disable", "Activate", "Link Mode ", 0, 1)
        self.link_mode_box.setFixedHeight(50)

        self.link_time_label = QLabel("Timer (*10ms) :")
        self.link_time_label.setFont(FontStyle.arial_font(True, False, 12))

        self.link_time_input = QLineEdit()
        self.link_time_input.setFixedWidth(250)
        # 默认值 2 = 延时 0 秒
        self.link_time_input.setText(str(config_manager.modbus_tcp.get("timer", 2)))

        self.setup_notice_timer = QPlainTextEdit()
        self.setup_notice_timer.setReadOnly(True)
        self.setup_notice_timer.setFixedHeight(150)
        self.setup_notice_timer.setFont(FontStyle.arial_font(False, False, 11))
        self.setup_notice_timer.setPlainText(
            "Link Time Reference\n"
            " 2    -> 0s    (immediate)\n"
            " 12   -> 0.1s  (very short)\n"
            " 52   -> 0.5s  (half second)\n"
            " 102  -> 1s    (1 second)\n"
            " 302  -> 3s    (3 seconds)\n"
        )
                
        self.modbus_test_btn = QPushButton("Test Connect")
        self.modbus_test_btn.setFixedSize(140, 40)
        self.modbus_test_btn.setIcon(QIcon("icons/refresh.svg"))
        self.modbus_test_btn.setIconSize(QSize(20, 20))

        self.modbus_save_btn = QPushButton("Save")
        self.modbus_save_btn.setFixedSize(120, 40)
        self.modbus_save_btn.setIcon(QIcon("icons/save.svg"))
        self.modbus_save_btn.setIconSize(QSize(20, 20))

        self.modbus_cancel_btn = QPushButton("Cancel")
        self.modbus_cancel_btn.setFixedSize(120, 40)
        self.modbus_cancel_btn.setIcon(QIcon("icons/cancel.svg"))
        self.modbus_cancel_btn.setIconSize(QSize(20, 20))

        self.ip_layout.addWidget(self.ip_label)
        self.ip_layout.addWidget(self.ip_input)
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addWidget(self.port_input)
        self.slave_layout.addWidget(self.slave_label)
        self.slave_layout.addWidget(self.slave_input)

        self.link_time_layout.addWidget(self.link_time_label)
        self.link_time_layout.addWidget(self.link_time_input)

        self.notice_timer_layout.addWidget(self.setup_notice_timer )

        self.save_layout.addStretch()
        self.save_layout.addWidget(self.modbus_test_btn)
        self.save_layout.addWidget(self.modbus_save_btn)
        self.save_layout.addWidget(self.modbus_cancel_btn)

        self.timer_start_layout.addWidget(self.inspection_timer_label)
        self.timer_start_layout.addWidget(self.inspection_timer_input)

        self.timer_leave_layout.addWidget(self.product_leave_label)
        self.timer_leave_layout.addWidget(self.product_leave_input)

        self.main_layout.addWidget(self.modbus_box)
        self.main_layout.addLayout(self.ip_layout)
        self.main_layout.addLayout(self.port_layout)
        self.main_layout.addLayout(self.slave_layout)
        self.main_layout.addLayout(self.timer_start_layout)
        self.main_layout.addLayout(self.timer_leave_layout)
        self.main_layout.addWidget(self.link_mode_box)
        self.main_layout.addLayout(self.link_time_layout)
        self.main_layout.addLayout(self.notice_timer_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.status_layout)
        self.main_layout.addLayout(self.save_layout)

        # ===== 根据 config 显示状态 =====
        if model_mode["modbus_tcp"] == 0:
            self.modbus_group.button(0).setChecked(True)
            self.show_fields(False)
        else:
            self.modbus_group.button(1).setChecked(True)
            self.show_fields(True)

        self.setLayout(self.main_layout)

        # ===== 信号连接 =====
        self.modbus_group.buttonClicked.connect(self.on_radio_changed)
        self.modbus_test_btn.clicked.connect(self.modbus_test_btn_clicked)
        self.modbus_save_btn.clicked.connect(self.modbus_save_btn_clicked)
        self.modbus_cancel_btn.clicked.connect(self.modbus_cancel_btn_clicked)
        self.link_mode_group.buttonClicked.connect(self.on_link_mode_changed)

        if config_manager.modbus_tcp.get("link_mode", 0) == 1:
            self.link_mode_group.button(1).setChecked(True)
        else:
            self.link_mode_group.button(0).setChecked(True)
            self.on_link_mode_changed()

    def show_fields(self, visible):
        self.ip_label.setVisible(visible)
        self.ip_input.setVisible(visible)
        self.port_label.setVisible(visible)
        self.port_input.setVisible(visible)
        self.slave_label.setVisible(visible)
        self.slave_input.setVisible(visible)
        self.link_mode_box.setVisible(visible)
        self.inspection_timer_label.setVisible(visible)
        self.inspection_timer_input.setVisible(visible)
        self.product_leave_input.setVisible(visible)
        self.product_leave_label.setVisible(visible)
        if not visible:
            self.link_time_label.setVisible(False)
            self.link_time_input.setVisible(False)
            self.setup_notice_timer.setVisible(False)
        else:
            # 恢复 Link Mode 的显示状态
            self.on_link_mode_changed()

    def on_radio_changed(self):
        checked = self.modbus_group.checkedId()
        if checked == 0:
            self.show_fields(False)
        elif checked == 1:
            self.show_fields(True)

    def on_link_mode_changed(self):
   
        checked = self.link_mode_group.checkedId()

        if checked == 0:
            self.link_time_label.setVisible(False)
            self.link_time_input.setVisible(False)
            self.setup_notice_timer.setVisible(False)
        elif checked == 1:
            self.link_time_label.setVisible(True)
            self.link_time_input.setVisible(True)
            self.setup_notice_timer.setVisible(True)       

    # ===== Cancel =====
    def modbus_cancel_btn_clicked(self):

        modbus_connecting_manager.modbus_disconnect()
        self.reject()
    # ===== Save =====
    def modbus_save_btn_clicked(self):
        try:
            enable = self.modbus_group.checkedId()
            ip = self.ip_input.text().strip()
            port = int(self.port_input.text().strip())
            slave_id = int(self.slave_input.text().strip())
            link_enable = self.link_mode_group.checkedId()
            link_time = int(self.link_time_input.text().strip())
            inspection_start = int(self.inspection_timer_input.text().strip())
            product_leave = int(self.product_leave_input.text().strip())

            
        except ValueError:
            QMessageBox.warning(self, "Warning", "Port / Slave ID / Link Time must be number")
            return

       
        config_manager.comm_mode["modbus_tcp"] = enable
        config_manager.modbus_tcp["ip_address"] = ip
        config_manager.modbus_tcp["port"] = port
        config_manager.modbus_tcp["slave_id"] = slave_id
        config_manager.modbus_tcp["link_mode"] = link_enable
        config_manager.modbus_tcp["timer"] = link_time
        config_manager.modbus_tcp["inspection_start"] = inspection_start
        config_manager.modbus_tcp["product_leave"] = product_leave
        

        config_manager.save_config()
        modbus_connecting_manager.modbus_disconnect()
        self.accept()

    def modbus_test_btn_clicked(self):

        try:

            ip = self.ip_input.text().strip()
            port = int(self.port_input.text().strip())
            link_enable = self.link_mode_group.checkedId()
            link_time = int(self.link_time_input.text().strip())

            result = modbus_connecting_manager.modbus_connecting()

            if result["status"] != "ok":
                QMessageBox.warning(self, "Test", result["message"])
                return

            link_enable = self.link_mode_group.checkedId()

            if link_enable == 1:
                link_time = int(self.link_time_input.text().strip())
                modbus_connecting_manager.write_register(0x00, 2)
                modbus_connecting_manager.write_register(0x63, link_time)
                QMessageBox.information(self, "Test",
                    f"{result['message']}\nLink Mode ON, delay = {(link_time-2)*0.01:.2f}s")
                
            elif link_enable == 0 :

                modbus_connecting_manager.write_register(0x00, 0)
                modbus_connecting_manager.write_register(0x63, 0)
                             
                QMessageBox.information(self, "Test",
                    f"Success: Connected to {ip}:{port}\n"
                    f"Link Mode Disable ")



        except Exception as e:
            QMessageBox.warning(self, "Test", f"Test failed: {e}")

        """
        Link Time 值	实际延时	用途
        2	0 秒	立即联动
        12	0.1 秒	极短延时
        52	0.5 秒	半秒延时
        102	1 秒	1秒延时
        302	3 秒	3秒延时
        """        