from PySide6.QtCore import QThread
from camera.signal_bus import signal_bus
from utils.config import config_manager
import cv2 as cv


class CameraThread(QThread):

    def __init__(self):
        super().__init__()
        self.running = True
        self.pause_emit = False
        self.is_camera_ok = False
        self.cap = None
        self.latest_frame = None

    def run(self):

        self.running = True

        # congig camera
        self.cap = cv.VideoCapture(config_manager.camera_index, cv.CAP_V4L2)
       
        self.cap.set(cv.CAP_PROP_AUTO_EXPOSURE, config_manager.auto_exposure )
        self.cap.set(cv.CAP_PROP_EXPOSURE, config_manager.exposure)
        self.cap.set(cv.CAP_PROP_AUTO_WB, config_manager.auto_white_balance)      # Auto White Balance OFF
        self.cap.set(cv.CAP_PROP_WB_TEMPERATURE, config_manager.white_balance_temperature)
        self.cap.set(cv.CAP_PROP_GAMMA, config_manager.gamma)
        self.cap.set(cv.CAP_PROP_CONTRAST,config_manager.contrast)
        self.cap.set(cv.CAP_PROP_SHARPNESS,config_manager.sharpness )
        self.cap.set(cv.CAP_PROP_FPS, 20)

        # checking camera  
        if not self.cap.isOpened():
            signal_bus.camera_status.emit(False)
            signal_bus.camera_error.emit("Please select a camera in Camera Settings.")
            return
        
        self.is_camera_ok = True
        signal_bus.camera_status.emit(True)

        try:
            while self.running and not self.isInterruptionRequested():

                success, frame = self.cap.read()

                if not success: #"跑一半断了"

                    self.is_camera_ok = False
                    # print("Camera disconnected")
                    signal_bus.camera_disconnected.emit() # 发断线信号
                    
                    signal_bus.camera_error.emit("Camera disconnected during run.")

                    break # 直接跳出循环，结束线程

                frame = cv.flip(frame, config_manager.camera_flip)
                
                self.latest_frame = frame


                if not self.pause_emit:
                    signal_bus.frame_ready.emit(frame)
                self.msleep(50)
              
        finally:
            if self.cap:
                self.cap.release()

    def stop(self):

        self.running = False
        self.requestInterruption()
        self.wait()
