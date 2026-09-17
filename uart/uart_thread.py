from PySide6.QtCore import QThread,QTimer
from camera.signal_bus import signal_bus
from connecting.uart_connecting_manager import uart_connecting_manager
import serial



class UARTThread(QThread):

    def __init__(self):
        super().__init__()

        self.running = False

    def run(self):

        # print("uart running")

        self.running = True

        while self.running:

            try:

                data = uart_connecting_manager.receiver()

                if data is None:
                    self.msleep(15)
                    continue
                self.on_uart_receive(data)
                
                self.msleep(5)

            except (serial.SerialException, OSError):

                signal_bus.uart_error.emit("UART disconnected during run")
                signal_bus.uart_disconnected.emit()
                break


    def stop(self):

        self.running = False

        self.wait()

    def on_uart_receive(self,data):

        if data is None:
            return
        
        text = data.decode("utf-8").strip()


        if text =="checking":
            self.msleep(100)
            signal_bus.uart_trigger.emit()

            

    def uart_send_data(self,result):
        self.msleep(100)
        uart_connecting_manager.send(result)
        
            