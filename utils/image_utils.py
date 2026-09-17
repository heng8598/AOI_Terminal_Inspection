from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QSize, Qt
import cv2 as cv

from pipeline.terminal_draw_tool import DrawTool
from utils.config import config_manager


draw = DrawTool()

def DisplayBGR2RGB(image, label):
    """
    把OpenCV的BGR图像显示到QLabel上
    image: cv的numpy数组
    label: PySide6的QLabel
    """
    if image is None:
        return

    if len(image.shape) == 2: # 灰度图
        h, w = image.shape
        # 注意: 灰度图bytesPerLine = w, 不是 w*1
        img = QImage(image.data, w, h, w, QImage.Format_Grayscale8).copy()
        target_size = QSize(300, 250)
    else: # 彩色图 BGR -> RGB
        
        if config_manager.debug["roi"]:
            draw.live_view_roi(image)

        if config_manager.debug["Level Line"]: 
            draw.level_line(image)  

        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        h, w, c = image.shape
        img = QImage(image.data, w, h, 3 * w, QImage.Format_RGB888).copy()
        target_size = QSize(640, 480)

        


    pixmap = QPixmap.fromImage(img)
    pix = pixmap.scaled(
        target_size,
        Qt.KeepAspectRatio,
        Qt.SmoothTransformation  
    )
    label.setPixmap(pix)

    
   