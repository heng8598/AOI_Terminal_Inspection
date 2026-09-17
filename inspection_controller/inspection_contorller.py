from pipeline.prosess_inspection import prosess_inspection
from camera.signal_bus import signal_bus
import cv2 as cv


class InspectionController():

    def __init__(self,camera_thread):


        signal_bus.inspection_request.connect(self.once_inspection)
        self.camera_thread = camera_thread


    def once_inspection(self):

        img = self.camera_thread.latest_frame.copy()

        # print(hash(img.tobytes()))
        
        result = prosess_inspection(img)
        # result = prosess_inspection_v2(img)
   
        signal_bus.inspection_result.emit(result)
        signal_bus.inspection_finish.emit()

      
