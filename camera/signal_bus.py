from PySide6.QtCore import Signal,QObject

class SignalBus(QObject):

    # ===== Camera =====
    frame_ready = Signal(object)
    camera_status = Signal(bool)
    camera_disconnected = Signal()
    camera_error = Signal(str)

    # ===== UART =====
    uart_error = Signal(str)
    uart_status = Signal(bool)
    uart_disconnected = Signal()
    uart_trigger = Signal()

    # ===== Modbus TCP =====
    modbus_trigger = Signal()
    modbus_error = Signal(str)
    modbus_disconnected = Signal()
    modbus_product_left = Signal()
    modbus_ng_result = Signal()

    # ===== State Machine =====
    error_state = Signal()
    state_machine_finish = Signal()
    state_camera_init = Signal()
    selected_mode_done = Signal()
    inspection_error = Signal()
    inspection_request = Signal()
    inspection_result = Signal(object)
    inspection_finish = Signal()
    auto_trigger = Signal()

    # ===== Others =====
    calibration_error = Signal(str)
    database_error = Signal(str)
    process_error = Signal(int, str)
    roi_position_setup = Signal(int, int, int, int)
  

signal_bus = SignalBus()