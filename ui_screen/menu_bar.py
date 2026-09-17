from PySide6.QtWidgets import QMainWindow,QMessageBox

# ===== 对话框 =====
from ui_screen.about_us import AboutUsDialog
from dialog.camera_setting_dialog import CameraSettingDialog
from dialog.roi_setting_dialog import ROISettingDialog
from dialog.debug import DebugDialog
from dialog.detection_parameter import DetectionParameters
from dialog.calibration import Calibration

from uart.uart import UARTDialog
from plc.modbus import ModbusTCPDialog

from utils.config import config_manager

#tool
from style.css_style import MyCSS

class MainMenuBar:

    def __init__(self,main_window : QMainWindow,camera_thread):
        self.main_window = main_window
        self.camera_thread =camera_thread


    def initialize(self):

        menu_bar = self.main_window.menuBar()
        menu_bar.setStyleSheet(MyCSS.MainMenuBar)

        # 5菜单
        # file_menu   = menu_bar.addMenu("File")
        setting_menu = menu_bar.addMenu("Setting")
        communication_menu = menu_bar.addMenu("Communication")
        inspection_menu = menu_bar.addMenu("Inspection")
        debug_menu  = menu_bar.addMenu("Debug")
        help_menu   = menu_bar.addMenu("Help")

        # File菜单
        # open_file = file_menu.addAction("Open file")
        # open_file.triggered.connect(self.open_file_clicked)
        
        # # File菜单
        # save_image = file_menu.addAction("Save Image")
        # save_image.triggered.connect(self.save_image_clicked)


        # Setting菜单
        camera_setting = setting_menu.addAction("Camera Setting")
        camera_setting.triggered.connect(self.camera_setting_clicked)


        # Setting子菜单：4路相机
        camera_select = setting_menu.addMenu("Camera Select")

        camera0 = camera_select.addAction("Camera 0")
        camera0.triggered.connect(lambda: self.camera_select_clicked(0))

        camera1 = camera_select.addAction("Camera 1")
        camera1.triggered.connect(lambda:self.camera_select_clicked(1))

        camera2 = camera_select.addAction("Camera 2")
        camera2.triggered.connect(lambda:self.camera_select_clicked(2))

        camera3 = camera_select.addAction("Camera 3")
        camera3.triggered.connect(lambda:self.camera_select_clicked(3))

        uart = communication_menu.addAction("Uart")
        uart.triggered.connect(self.uart_clicked)

        modbus = communication_menu.addAction("Modbus")
        modbus.triggered.connect(self.modbus_clicked)

        
        parameter = inspection_menu.addAction("Detection Parameters")
        parameter.triggered.connect(self.parameter_clicked)

        calibration = inspection_menu.addAction("Calibration")
        calibration.triggered.connect(self.calibration_clicked)

        #setting roi setup
        roi_setting_action = setting_menu.addAction("ROI Setting" )
        roi_setting_action.triggered.connect(self.roi_setting_clicked)

        #setting debug setup
        debug_display = debug_menu.addAction("debug display" )
        debug_display.triggered.connect(self.debug_display_clicked)


        #setting help setup
        about_us = help_menu.addAction("About Us")
        about_us.triggered.connect(self.show_about_dialog)
            


    # def open_file_clicked(self):
    #     pass
    # def save_image_clicked(self):
    #     pass

    def camera_setting_clicked(self):

        dialog_camera_setting = CameraSettingDialog(self.main_window)

        dialog_camera_setting.exec()

    def camera_select_clicked(self,camera_index):

        self.camera_index = camera_index 

        config_manager.camera_index = self.camera_index 

        config_manager.save_config()

        print(self.camera_index)

    def uart_clicked(self):

        model_mode = config_manager.comm_mode
                
        if model_mode["modbus_tcp"] == 1:
            QMessageBox.warning(self.main_window,"Warning","Please disable Modbus TCP Mode.")
            return

        dialog_uart = UARTDialog(self.main_window)  
        dialog_uart.exec()  

    def modbus_clicked(self):

        model_mode = config_manager.comm_mode
        
        if model_mode["uart"] == 1:
            QMessageBox.warning(self.main_window,"Warning","Please disable UART Mode.")
            return

        dialog_modbus_tcp = ModbusTCPDialog(self.main_window)

        dialog_modbus_tcp.exec()

    def parameter_clicked(self):
        
        dialog_parameters = DetectionParameters(self.main_window)

        dialog_parameters.exec()

    def calibration_clicked(self):

        dialog_calibration = Calibration(self.main_window)

        dialog_calibration.show()

    def roi_setting_clicked(self):

        dialog_roi_setting = ROISettingDialog(self.main_window,self.camera_thread)

        dialog_roi_setting.exec()

    def debug_display_clicked(self):
        
        dialog_debug =DebugDialog(self.main_window)
        dialog_debug.exec()

    def show_about_dialog(self):

        dialog_about_us = AboutUsDialog(self.main_window)
        dialog_about_us.exec()

