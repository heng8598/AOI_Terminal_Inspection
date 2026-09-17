from PySide6.QtCore import QThread
from camera.signal_bus import signal_bus
from connecting.modbus_connecting_manager import modbus_connecting_manager
from utils.config import config_manager


class ModbusTCPThread(QThread):

    def __init__(self):
        super().__init__()
        self.running = False
        self.poll_interval = 15
        self.start_timer = config_manager.modbus_tcp["inspection_start"]
        self.product_leave = config_manager.modbus_tcp["product_leave"]

        # 产品状态
        # "WAIT_PRODUCT"  → 等产品到位
        # "PRODUCT_PRESENT" → 产品在位，正在检测
        self.product_state = "WAIT_PRODUCT"

        # 上一次 IN1 状态
        self.last_in1_state = False

    def run(self):

        self.running = True

        while self.running:
            try:
                # 1. 读 IN1 状态
                result = modbus_connecting_manager.read_inputs(0, 1)
                
                if result is None or result.isError():
                    self.msleep(self.poll_interval)
                    continue

                in1 = result.bits[0]
           

                # 2. 状态机
                if self.product_state == "WAIT_PRODUCT":
                    # 等待上升沿（产品到位）
                    if in1 and not self.last_in1_state:
                        self.on_product_arrived()
                        self.product_state = "PRODUCT_PRESENT"

                elif self.product_state == "PRODUCT_PRESENT":
                    # 产品在位，等待下降沿（产品离开）
                    if not in1 and self.last_in1_state:
                        self.on_product_left()
                        self.product_state = "WAIT_PRODUCT"

                # 3. 保存状态
                self.last_in1_state = in1

                # 4. 轮询间隔
                self.msleep(self.poll_interval)

            except Exception as e:
                signal_bus.modbus_error.emit(f"Modbus TCP error: {str(e)}")
                signal_bus.modbus_disconnected.emit()
                break

    def stop(self):
        self.running = False
        self.wait()

    def on_product_arrived(self):
        """产品到位 → 触发 AOI 检测"""
        self.msleep(self.start_timer)   # 等灯稳定
        signal_bus.modbus_trigger.emit()

    def on_product_left(self):
        """产品离开 → 通知状态机"""
        self.msleep(self.product_leave) 
        signal_bus.modbus_product_left.emit()

    def reset_trigger(self):
        """强制重置状态（用于异常恢复）"""
        self.product_state = "WAIT_PRODUCT"
        self.last_in1_state = False
   
    