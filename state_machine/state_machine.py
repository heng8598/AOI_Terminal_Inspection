from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QMessageBox
from PySide6.QtStateMachine import QStateMachine, QState,QSignalTransition

from camera.signal_bus import signal_bus
from connecting.uart_connecting_manager import uart_connecting_manager
from connecting.modbus_connecting_manager import modbus_connecting_manager

class StateMachine(QStateMachine):

    # Internal signal for StateMachine
    camera_error_signal = Signal()

    def __init__(self, left_panel, system_status, camera_thread,uart_thread,modbus_thread,label_inspection_show):

        super().__init__()
        self.last_result = None
        self.is_ng = False
        self.left_panel = left_panel
        self.system_status = system_status
        self.camera_thread = camera_thread
        self.uart_thread = uart_thread
        self.modbus_thread = modbus_thread
        self.inspection_show = label_inspection_show

        self.current_mode = None

        # ---------------- States ----------------
        self.state_idle = QState(self)
        self.state_camera_init = QState(self)
        self.state_waiting_mode = QState(self)
        self.state_wating_trigger = QState(self)
        self.state_inspection_start = QState(self)
        self.state_error = QState(self)

        self.state_idle.entered.connect(self.setup_idle)
        self.state_camera_init.entered.connect(self.camera_init)
        self.state_waiting_mode.entered.connect(self.wating_mode)
        self.state_wating_trigger.entered.connect(self.wating_trigger)
        self.state_inspection_start.entered.connect(self.inspection_start)
        self.state_error.entered.connect(self.setup_error)
        
     

        # ---------------- Transitions ----------------

        # Idle -> camera init
        self.state_idle.addTransition(self.left_panel.buttons["start"].clicked,self.state_camera_init)

        # camera init -> Idle
        self.state_camera_init.addTransition(self.left_panel.buttons["stop"].clicked,self.state_idle)

        #camera init -> wating mode
        self.state_camera_init.addTransition(signal_bus.state_camera_init,self.state_waiting_mode)

        # wati_mode -> idle
        self.state_waiting_mode.addTransition(self.left_panel.buttons["stop"].clicked,self.state_idle)
        
        # mode selected done
        self.state_waiting_mode.addTransition(self.left_panel.buttons["manual"].clicked,self.state_wating_trigger)
        self.state_waiting_mode.addTransition(self.left_panel.buttons["auto"].clicked,self.state_wating_trigger)
        self.state_waiting_mode.addTransition(self.left_panel.buttons["uart"].clicked,self.state_wating_trigger)
        self.state_waiting_mode.addTransition(self.left_panel.buttons["modbus"].clicked,self.state_wating_trigger)

        # waiting trigger - Idle
        self.state_wating_trigger.addTransition( self.left_panel.buttons["stop"].clicked,self.state_idle)

        # waiting trigger -> Inspection 
        self.state_wating_trigger.addTransition(self.left_panel.buttons["manual"].clicked,self.state_inspection_start)
        self.state_wating_trigger.addTransition(signal_bus.auto_trigger,self.state_inspection_start)
        self.state_wating_trigger.addTransition(signal_bus.uart_trigger,self.state_inspection_start)
        self.state_wating_trigger.addTransition(signal_bus.modbus_trigger,self.state_inspection_start)


        #inpection -. waiting trigger
        self.state_inspection_start.addTransition(signal_bus.inspection_finish,self.state_wating_trigger)

        self.state_inspection_start.addTransition(self.left_panel.buttons["stop"].clicked,self.state_idle)

        # Error -> Idle
        self.state_error.addTransition(self.left_panel.buttons["stop"].clicked,self.state_idle)

        # Running -> Error
        self.state_inspection_start.addTransition(signal_bus.camera_disconnected,self.state_error)
        self.state_wating_trigger.addTransition(signal_bus.camera_disconnected,self.state_error)

        self.state_inspection_start.addTransition(signal_bus.uart_disconnected,self.state_error)
        self.state_wating_trigger.addTransition(signal_bus.uart_disconnected,self.state_error)

        self.state_inspection_start.addTransition(signal_bus.modbus_disconnected,self.state_error)
        self.state_wating_trigger.addTransition(signal_bus.modbus_disconnected,self.state_error)

        self.state_inspection_start.addTransition(signal_bus.error_state,self.state_error)
        self.state_wating_trigger.addTransition(signal_bus.error_state,self.state_error)


        # ---------------- Mode ----------------
        self.left_panel.buttons["manual"].clicked.connect(self.select_manual_mode)

        self.left_panel.buttons["auto"].clicked.connect(self.select_auto_mode)

        self.left_panel.buttons["uart"].clicked.connect(self.select_uart_mode)

        self.left_panel.buttons["modbus"].clicked.connect( self.select_modbus_mode)

        # ---------------- Camera ----------------

        signal_bus.camera_status.connect(self.on_camera_status_check)

        signal_bus.inspection_finish.connect(self.inspection_finish)

        signal_bus.inspection_result.connect(self.on_inspetion_result)

        signal_bus.modbus_product_left.connect(self.on_modbus_product_left)

        self.setInitialState(self.state_idle)
        self.start()

    # ------------------------------------------------

    def setup_idle(self):

   
        self.current_mode = None

        if self.camera_thread.isRunning():
            signal_bus.frame_ready.emit(None)
            self.camera_thread.stop()
            self.inspection_show.inspection_stop_label()

        # uart stop
        if self.uart_thread.isRunning():
            self.uart_thread.stop()
            self.inspection_show.inspection_stop_label()

        if self.modbus_thread.isRunning():  
            self.modbus_thread.stop() 
            self.inspection_show.inspection_stop_label() 

        modbus_connecting_manager.modbus_disconnect()
        uart_connecting_manager.uart_disconnect()

        for btn in self.left_panel.buttons.values():
            btn.setEnabled(False)

        self.left_panel.buttons["start"].setEnabled(True)
        

        labels = ["camera","manual","auto", "uart", "modbus"]

        for label in labels:
            self.system_status.update_system_status(label, "")


    def camera_init(self):

        # print("camera_init")

        for btn in self.left_panel.buttons.values():
            btn.setEnabled(True)
  

        if not self.camera_thread.isRunning():
            self.system_status.update_system_status("camera","Checking...")
            self.camera_thread.start()


    def on_camera_status_check(self, is_ok):

        if self.state_camera_init not in self.configuration():
            return
        
        if is_ok:

            for btn in self.left_panel.buttons.values():
                btn.setEnabled(True)

            self.left_panel.buttons["start"].setEnabled(False)
            self.left_panel.buttons["stop"].setEnabled(True)
            signal_bus.state_camera_init.emit()

            # print("camera start")
              
            self.system_status.update_system_status("camera", "OK")
            
        else:
            signal_bus.camera_disconnected.emit()   

    def wating_mode(self):

        for btn in self.left_panel.buttons.values():
            btn.setEnabled(True)
        self.left_panel.buttons["start"].setEnabled(False)  

    def wating_trigger(self):

        # print("wating trigger")  

        for btn in self.left_panel.buttons.values():
            btn.setEnabled(False)

        self.left_panel.buttons["stop"].setEnabled(True)
        self.left_panel.buttons[self.current_mode].setEnabled(True)

        self.system_status.update_system_status(self.current_mode,"OK")



    def inspection_start(self):


        for btn in self.left_panel.buttons.values():
            btn.setEnabled(False)

        self.left_panel.buttons["stop"].setEnabled(True)

        signal_bus.inspection_request.emit()
        
    def inspection_finish(self):


        if self.current_mode == "uart":

            if not self.is_ng:
                self.uart_thread.uart_send_data("OK")
                return
            else :
                self.uart_thread.uart_send_data("NG")
     
        elif self.current_mode == "auto":
            
            QTimer.singleShot(400, signal_bus.auto_trigger.emit)
         
            
    # ------------------------------------------------

    def setup_error(self):

        # print("Enter Error")

        self.system_status.update_system_status("camera" ,"ERROR")
        self.system_status.update_system_status(self.current_mode ,"ERROR")

        for btn in self.left_panel.buttons.values():
            btn.setEnabled(False)

        self.left_panel.buttons["stop"].setEnabled(True)
        
        QTimer.singleShot( 500, lambda: self.left_panel.buttons["stop"].click())


    def select_manual_mode(self):

        self.current_mode = "manual"
        
    def select_auto_mode(self):
        
        self.current_mode = "auto"

        QTimer.singleShot( 400,signal_bus.auto_trigger.emit)


    def select_uart_mode(self):

        self.current_mode = "uart"

        self.system_status.update_system_status(self.current_mode,"....")

        uart_result = uart_connecting_manager.uart_connecting()


        if uart_result.get("status") == "failed":

            signal_bus.uart_error.emit(uart_result.get("message"))

            signal_bus.error_state.emit()

            return
        self.system_status.update_system_status(self.current_mode,uart_result.get("message"))
        self.uart_thread.start()
        # print("uart start")

    def select_modbus_mode(self):

        self.current_mode = "modbus"

        self.system_status.update_system_status(self.current_mode,"....")
        
        modbus_result = modbus_connecting_manager.modbus_connecting() 
 
        if modbus_result.get("status") == "failed":
        
            signal_bus.modbus_error.emit(modbus_result.get("message"))

            signal_bus.error_state.emit()

            return
        self.system_status.update_system_status(self.current_mode,modbus_result.get("message"))
        self.modbus_thread.start() 

    def on_inspetion_result(self,result):

        self.last_result = result
        self.is_ng = self.check_is_ng(result)

    def check_is_ng(self, result):

        if result is None:
            return True

        inspection = result

        pin_missing = inspection.get("missing", [])

        if len(pin_missing):
            return True    
        for terminal in result.get("result", []):

            pin = terminal["pin_result"]["pin"]

            if pin["A"] != 1 or pin["B"] != 1:
                return True

            width = terminal["width_termianl"]
            angle = terminal["angle_terminal"]

            if width.get("status_width") == "NG":
                return True
            if angle.get("status_angle") == "NG":
                return True

        return False

    def stop_blow(self):

        modbus_connecting_manager.write_coil(1, False) 
    

    def on_modbus_product_left(self):

        if self.current_mode != "modbus":
            return

        if not self.is_ng:
            return

        modbus_connecting_manager.write_coil(1, True)   # CH02 开
        QTimer.singleShot(300, self.stop_blow)