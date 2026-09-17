
import serial
from utils.config import config_manager
from camera.signal_bus import signal_bus

class UartConnectingManager:

    def __init__(self):

        self.serial = None
        
    def uart_connecting(self):
    
        module_name = "uart_connecting"

        comm_model = config_manager.comm_mode["uart"]
        uart_baud = config_manager.uart["baudrate"]
        comm_port = config_manager.uart["com_port"]

        if self.serial is not None:
            # print("enter uart")

            if self.serial.is_open:
                return {
                        "module_name": module_name,
                        "status": "ok",
                        "message": "UART already connected."
                    }

        if comm_model != 1:

            return {
                    "module_name" : module_name,
                    "status": "failed",
                    "message": "UART is not configured."
                    }
                        
        try:
            self.serial = serial.Serial(port=comm_port, baudrate=uart_baud, timeout=0.1)

            if self.serial.is_open:
                # print("connect uart")
                return {
                    "module_name" : module_name,
                    "status": "ok",
                    "message": "UART connected successfully."
                    }

        except serial.SerialException as e:
    
                    return{
                            "module_name" : module_name,
                            "status": "failed",
                            "message": str(e)
                            }
        

    def uart_disconnect(self):

        module_name = "uart_disconnect"

        if self.serial and self.serial.is_open:
            self.serial.close()

        self.serial = None

        return{
             "module_name" : module_name,
             "status": "ok"
               }
    
    def receiver(self):

        if self.serial is None:

            raise serial.SerialException("UART not connected")

        try:

            if self.serial.in_waiting == 0:
                return None

            return self.serial.readline()

        except (serial.SerialException, OSError):
            raise
            
    def send(self, data):

        if isinstance(data, str):
            data = data.encode("utf-8")

        self.serial.write(data)

uart_connecting_manager = UartConnectingManager()