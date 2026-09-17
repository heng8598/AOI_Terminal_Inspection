from pymodbus.client import ModbusTcpClient
from utils.config import config_manager


class ModbusConnectingManager:

    def __init__(self):
        self.client = None
        self.ip_address = None
        self.port = None
        self.slave_id = None

    def modbus_connecting(self):
        """
        Connect to Modbus TCP device.
        """
        module_name = "modbus_connecting"

        comm_model = config_manager.comm_mode["modbus_tcp"]
        self.ip_address = config_manager.modbus_tcp["ip_address"]
        self.port = config_manager.modbus_tcp["port"]
        self.slave_id = config_manager.modbus_tcp["slave_id"]

        # Already connected?
        if self.client is not None:
            if self.client.is_socket_open():
                return {"module_name": module_name,"status": "ok","message": "Modbus TCP already connected."}

        # Not configured?
        if comm_model != 1:
            return {"module_name": module_name,"status": "failed","message": "Modbus TCP is not configured."}

        try:
            self.client = ModbusTcpClient(self.ip_address, port=self.port)
            if self.client.connect():
                return {"module_name": module_name,"status": "ok","message": f"Modbus TCP connected to {self.ip_address}:{self.port}"}
            else:
                self.client = None
                return {"module_name": module_name,"status": "failed","message": f"Cannot connect to {self.ip_address}:{self.port}"}

        except Exception as e:
            self.client = None
            return {
                "module_name": module_name,
                "status": "failed",
                "message": str(e)
            }

    def modbus_disconnect(self):
        """
        Disconnect from Modbus TCP device.
        """
        module_name = "modbus_disconnect"

        if self.client and self.client.is_socket_open():
            self.client.close()

        self.client = None

        return {
            "module_name": module_name,
            "status": "ok",
            "message": "Modbus TCP disconnected."
        }

    def is_connected(self):
        """Check if client is connected."""
        if self.client is None:
            return False
        return self.client.is_socket_open()

    
    def read_inputs(self, address=0, count=4):
            """
            Read discrete inputs.
            Default: read IN1~IN4.
            """
            if self.client is None:
                raise ConnectionError("Modbus TCP not connected")
    
            try:
                return self.client.read_discrete_inputs(address, count, slave= self.slave_id)
            except Exception as e:
                raise

    def write_coil(self, address, state):
        """
        Write a single coil (relay).
        address: coil address (0~63)
        state: True (ON) / False (OFF)
        """
        if self.client is None:
            raise ConnectionError("Modbus TCP not connected")

        try:
            return self.client.write_coil(address, state, slave = self.slave_id)
        except Exception as e:
            raise

    def read_coils(self, address, count):
        """
        Read coil states.
        address: start address
        count: number of coils
        """
        if self.client is None:
            raise ConnectionError("Modbus TCP not connected")

        try:
            return self.client.read_coils(address, count, slave = self.slave_id)
        except Exception as e:
            raise


    def read_registers(self, address, count):
        """
        Read holding registers.
        """
        if self.client is None:
            raise ConnectionError("Modbus TCP not connected")

        try:
            return self.client.read_holding_registers(address, count, slave = self.slave_id)
        except Exception as e:
            raise        
        
    def write_register(self,address, state):

        if self.client is None:
            raise ConnectionError("Modbus TCP not connected")

        try:
            return self.client.write_register(address, state, slave = self.slave_id)
        except Exception as e:
            raise
        

        
modbus_connecting_manager = ModbusConnectingManager()