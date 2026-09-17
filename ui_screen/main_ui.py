from PySide6.QtWidgets import QMainWindow,QHBoxLayout,QWidget,QVBoxLayout,QMessageBox
from PySide6.QtCore import Qt

#tool
from style.css_style import MyCSS

# screen qwidget
from ui_screen.menu_bar import MainMenuBar
from ui_screen.live_view_panel import LiveViewPanel
from camera.camera_thread import CameraThread
from ui_screen.inspection_view_panel import InspectionViewPanel
from ui_screen.left_panel import LeftButtonPanel
from ui_screen.counter_result import CounterResultLable
from ui_screen.final_result_valve import FinalResultValveTable
from ui_screen.status_system import SystemStatus
from ui_screen.ng_history_panel import NgHistoryRecord


#state machine
from state_machine.state_machine import StateMachine
from camera.signal_bus import signal_bus
from connecting.uart_connecting_manager import uart_connecting_manager
from inspection_controller.inspection_contorller import InspectionController
from pipeline.prosess_inspection import prosess_inspection


# commnucation
from uart.uart_thread import UARTThread
from plc.modbus_thread import ModbusTCPThread

import serial

from utils.config import config_manager

from counter.counter import Counter

ok_count = Counter()
ng_count = Counter()
total_count = Counter()

class MyMainPage(QMainWindow):

    MAIN_WINDOW_WIDTH = 1680
    MAIN_WINDOW_HEIGHT = 1050

    def __init__(self):

        self.camera_thread = None

        super().__init__()

        self.setWindowTitle("AOI Terminal Inspection System")
        self.resize(self.MAIN_WINDOW_WIDTH, self.MAIN_WINDOW_HEIGHT)
        self.setObjectName("MainBackGround")
        self.setStyleSheet(MyCSS.MainCSS + MyCSS.LEFT_PANEL_STYLE)


        config_manager.load_config()

        main_container = QWidget() # main 容器

        self.menu_bar = MainMenuBar(self,self.camera_thread)
        self.menu_bar.initialize()

        self.live_view_panel = LiveViewPanel(self)
        self.live_view_panel.initialize()

        self.camera_thread = CameraThread()
        signal_bus.frame_ready.connect(self.live_view_panel.update_frame)
        self.inspection_controller = InspectionController(self.camera_thread)

        self.uart_thread = UARTThread()

        self.inspection_view_panel = InspectionViewPanel(self)
        self.inspection_view_panel.initialize()

        self.modbus_thread = ModbusTCPThread()
        
        self.left_panel = LeftButtonPanel(self)
        self.left_panel.initialize()

        self.check_counter_lable = CounterResultLable(self,ok_count,ng_count,total_count)
        self.check_counter_lable.initialize()
  
        self.final_result_table = FinalResultValveTable(self)
        self.final_result_table.initialize()

        self.system_status = SystemStatus(self)
        self.system_status.initialize()

        self.history_ng_record = NgHistoryRecord(self)
        self.history_ng_record.initialize()

        self.system_final_resut_layout = QHBoxLayout()
        self.system_final_resut_layout.addWidget(self.final_result_table)
        self.system_final_resut_layout.addWidget(self.history_ng_record)
        self.system_final_resut_layout.addWidget(self.system_status)
        self.system_final_resut_layout.addStretch()



        left_panel_layout = QVBoxLayout()
        left_panel_layout.addWidget(self.left_panel)
        
        live_inspection_layout = QHBoxLayout() 
        live_inspection_layout.addWidget(self.live_view_panel ) 
        live_inspection_layout.addWidget(self.inspection_view_panel)
        live_inspection_layout.addStretch()


        counter_result_layout = QVBoxLayout()
        counter_result_layout.addWidget(self.check_counter_lable, alignment= Qt.AlignLeft)
        counter_result_layout.addLayout(self.system_final_resut_layout)


        join_counter_live_inspection = QVBoxLayout()
        join_counter_live_inspection.setSpacing(10)
        join_counter_live_inspection.addLayout(live_inspection_layout)
        join_counter_live_inspection.addLayout(counter_result_layout)
        join_counter_live_inspection.addStretch()


        main_layout = QHBoxLayout()
        main_layout.addLayout(left_panel_layout)
        main_layout.addLayout(join_counter_live_inspection)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(40)
       
        
        main_container.setLayout(main_layout) # 5. 把布局给容器
        self.setCentralWidget(main_container) # 6. 把容器给窗口

        self.machine = StateMachine(self.left_panel ,self.system_status,self.camera_thread,
                                    self.uart_thread,self.modbus_thread,self.inspection_view_panel)

        ground = ["-", "-", "-", "-", "-"]
        live = ["-", "-", "-", "-", "-"]
        neutral = ["-", "-", "-", "-", "-"]
        self.final_result_table.update_pin_result(ground,live,neutral)

        signal_bus.camera_error.connect(lambda msg: self.show_error_box("Camera Error", msg))

        signal_bus.uart_error.connect(lambda msg: self.show_error_box("Uart Error", msg))

        signal_bus.calibration_error.connect(lambda msg: self.show_error_box("Calibration Error", msg))

        signal_bus.inspection_result.connect(self.inpection_result)



    def show_error_box(self, title, msg):

        QMessageBox.critical(self, title, msg)

    def inpection_result(self,result):

        total_count.inc()
        self.check_counter_lable.check_counter_value_label.setText(str(total_count.get()))

        ground = ["-", "-", "-", "-", "-"]
        live = ["-", "-", "-", "-", "-"]
        neutral = ["-", "-", "-", "-", "-"]

        table = {"ground":ground, "live":live,"neutral":neutral }
  
        self.inspection_view_panel.inspection_view_display_show.clear()
        inspection = result
        #version 1 use
        terminals = inspection["result"]

        # version 2 use
        # terminals = inspection["result"]

        pin_missing = inspection.get("missing", [])
        img = inspection["missing_img"] if len(pin_missing) else inspection["draw_image"]["img"]
        image_status = "OK"


        if len(pin_missing):

            for terminal in terminals:

                name = terminal["name"]
                pin = terminal["pin_result"]["pin"]

                table[name][0] = "OK" if pin["A"] == 1 else "NG"
                table[name][1] = "OK" if pin["B"] == 1 else "NG"
           
                if table[name][0] == "OK" and table[name][1] == "OK":
                    
                    table[name][4] = "OK"
                else:
                    table[name][4] = "NG"
                    ng_count.inc()

                if pin["A"] != 1:
                    self.history_ng_record.add_ng_log(name, "Pin A Missing")

                if pin["B"] != 1:
                    self.history_ng_record.add_ng_log(name, "Pin B Missing")  

            self.check_counter_lable.ng_counter_value_label.setText(str(ng_count.get()))
  
        else:
            for terminal in terminals:

                name = terminal["name"]
                 
                pin = terminal["pin_result"]["pin"]
                width_terminal = terminal["width_termianl"]
                angle_terminal = terminal["angle_terminal"]
                width = width_terminal["width_text"]
                angle = angle_terminal["angle_text"]
                status_width = width_terminal["status_width"]
                status_angle = angle_terminal["status_angle"]

                statuses = ["OK" if pin["A"] == 1 else "NG",
                            "OK" if pin["B"] == 1 else "NG",
                            status_width,
                            status_angle,

                            ]
                
                table[name][0] = statuses[0]
                table[name][1] = statuses[1]
                table[name][2] = width
                table[name][3] = angle

                if all(s == "OK" for s in statuses):
                    table[name][4] = "OK"

                else:
                    table[name][4] = "NG"
                    image_status = "NG" 
                if status_width != "OK":

                    self.history_ng_record.add_ng_log(name, "Width NG")
    
                if status_angle != "OK":

                    self.history_ng_record.add_ng_log(name, "Angle NG")  

                  

            if image_status == "OK":
                ok_count.inc()
                self.check_counter_lable.ok_counter_value_label.setText(str(ok_count.get()))
            else:
                ng_count.inc()
                self.check_counter_lable.ng_counter_value_label.setText(str(ng_count.get()))
                

        # print(table)
        self.final_result_table.update_pin_result(ground,live,neutral)
        self.inspection_view_panel.update_frame(img)
        self.check_counter_lable.update_yield()      


    def closeEvent(self, event):

        try:

            threads = [self.camera_thread,self.uart_thread,self.modbus_thread]

            for thread in threads:

                if thread is None:
                    continue

                thread.stop()

                if not thread.wait(3000):
                    print(f"{thread.__class__.__name__} did not stop")

            uart_connecting_manager.uart_disconnect()

        except Exception as e:
            print(e) 

        event.accept()



