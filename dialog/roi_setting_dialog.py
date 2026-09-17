from PySide6.QtWidgets import QDialog,QGroupBox, QHBoxLayout,QRadioButton,\
                                QVBoxLayout,QPushButton,QMessageBox,QButtonGroup,QLabel
from PySide6.QtCore import Qt,QRect,QSize
from PySide6.QtGui import QPainter,QPen,QIcon

from camera.signal_bus import signal_bus
from utils.image_utils import DisplayBGR2RGB
from utils.config import config_manager
from style.css_style import MyCSS



class ROISettingDialog(QDialog):

    def __init__(self,camera_thread = None,parent=None):

        super().__init__(parent) 

        self.camera_thread =camera_thread
        self.current_frame = None

        signal_bus.frame_ready.connect(self.update_frame)
        
        self.drawing_mode = False

        self.setWindowTitle("ROI Setting")
        self.setFixedSize(650, 700)

        self.radio_layout = QHBoxLayout()
        self.draw_layout = QHBoxLayout()
        self.roi_result_layout = QHBoxLayout()
        


        self.grounding_roi = QRadioButton("Ground ROI")
        self.grounding_roi.setChecked(True)

        self.live_roi = QRadioButton("Live ROI")
        self.neutral_roi = QRadioButton("Neutral ROI")

        self.radio_layout.addWidget(self.grounding_roi)
        self.radio_layout.addWidget(self.live_roi)
        self.radio_layout.addWidget(self.neutral_roi)
        


        self.btn_group = QGroupBox("ROI Setup")
        self.btn_group.setStyleSheet(MyCSS.GROUP_BOX_STYLE) 
        self.btn_group.setLayout(self.radio_layout)

        #input img
        self.roi_img = RoiImageLabel()#input frame for draw roi
        self.roi_img.setFixedSize(640,480)
        self.roi_img.setContentsMargins(0, 0, 0, 0)
        self.roi_img.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.roi_img.setStyleSheet("margin:0px; padding:0px;")
     
        # BUTTON
        self.roi_draw_btn = QPushButton("Draw")
        self.roi_draw_btn.setFixedSize(120, 40)
        self.roi_draw_btn.setIcon(QIcon("icons/pencil.svg"))
        self.roi_draw_btn.setIconSize(QSize(20, 20))


        self.roi_start_btn = QPushButton("Start")
        self.roi_start_btn.setFixedSize(120, 40)
        self.roi_start_btn.setIcon(QIcon("icons/play.svg"))
        self.roi_start_btn.setIconSize(QSize(20, 20))


        self.roi_save_btn = QPushButton("Save")
        self.roi_save_btn.setFixedSize(120, 40)
        self.roi_save_btn.setIcon(QIcon("icons/save.svg"))
        self.roi_save_btn.setIconSize(QSize(20, 20))


        self.roi_cancel_btn = QPushButton("Cancel")
        self.roi_cancel_btn.setFixedSize(120, 40)
        self.roi_cancel_btn.setIcon(QIcon("icons/cancel.svg"))
        self.roi_cancel_btn.setIconSize(QSize(20, 20))


        self.draw_layout.addWidget(self.roi_draw_btn)
        self.draw_layout.addWidget(self.roi_start_btn)
        self.draw_layout.addWidget(self.roi_save_btn)
        self.draw_layout.addWidget(self.roi_cancel_btn)


        self.roi_result_box = QGroupBox("Region Of Interest") 
        self.roi_result_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        self.roi_result_box.setFixedSize(640,60)

        self.roi_result_label = QLabel()
        self.roi_result_label.setStyleSheet("color : black")
        
        self.roi_result_layout.addWidget(self.roi_result_label)
        self.roi_result_box.setLayout(self.roi_result_layout)

        self.groud_all_layout = QVBoxLayout()
        self.groud_all_layout.addWidget(self.btn_group,alignment=Qt.AlignTop)
        self.groud_all_layout.addWidget(self.roi_img, alignment=Qt.AlignCenter)
        self.groud_all_layout.addStretch()
        self.groud_all_layout.addWidget(self.roi_result_box)
        self.groud_all_layout.addLayout(self.draw_layout)

        self.setLayout(self.groud_all_layout)

        self.roi_group_btn = QButtonGroup(self)
        self.roi_group_btn.addButton(self.grounding_roi,1)
        self.roi_group_btn.addButton(self.live_roi,2)
        self.roi_group_btn.addButton(self.neutral_roi,3)

        signal_bus.roi_position_setup.connect(self.get_roi_valve)

        self.roi_draw_btn.clicked.connect(self.roi_draw_click)
        self.roi_start_btn.clicked.connect(self.roi_start_click)
        self.roi_save_btn.clicked.connect(self.roi_save_click)
        self.roi_cancel_btn.clicked.connect(self.roi_cancel_click)

    

    def roi_draw_click(self):

        self.drawing_mode = True

        self.roi_img.start_point = None
        self.roi_img.end_point = None

        self.roi_img.setCursor(Qt.CrossCursor)


    def roi_start_click(self):

        if self.current_frame is None:
            return

        self.camera_thread.pause_emit = True

        img = self.current_frame.copy()

        DisplayBGR2RGB(img, self.roi_img)

        self.drawing_mode = True
        self.roi_img.setMouseTracking(True) 
        self.roi_img.setCursor(Qt.CrossCursor)

    def roi_save_click(self):

        if self.camera_thread is not None:
            self.camera_thread.pause_emit = False
  

        config_manager.save_config()    

        reply = QMessageBox.question(self,"Save ROI",
                                    "ROI saved successfully.\n\nContinue editing ROI?",
                                        QMessageBox.Yes | QMessageBox.No
                                    )
        

        if reply == QMessageBox.No:
            self.drawing_mode = False    
            self.clear_image()
            
            self.roi_img.setMouseTracking(False)
            self.roi_img.unsetCursor()
            self.accept()
        

        
    def roi_cancel_click(self):

        if self.camera_thread is not None:
            self.camera_thread.pause_emit = False
        self.drawing_mode = False    
        self.clear_image()
        
        self.roi_img.setMouseTracking(False)
        self.roi_img.unsetCursor()
        self.reject()


    def clear_image(self):

        self.roi_img.clear()

        self.roi_img.start_point = None
        self.roi_img.end_point = None

        self.current_frame = None

        self.roi_img.update()
   
    def get_roi_valve(self,x,y,w,h):

        get_id_roi = self.roi_group_btn.checkedId()

        if get_id_roi == 1:
           
           config_manager.ground_roi = {
            "x": x,
            "y": y,
            "w": w,
            "h": h
            }
 
           self.roi_result_label.setText(f"Ground x:{x}, y:{y}, w:{w}, h:{h}")
           
        if get_id_roi == 2:   

            config_manager.live_roi = {
            "x": x,
            "y": y,
            "w": w,
            "h": h
            }
            
  
            self.roi_result_label.setText(f"Live x:{x}, y:{y}, w:{w}, h:{h}")

        if get_id_roi == 3:   

            config_manager.neutral_roi = {
            "x": x,
            "y": y,
            "w": w,
            "h": h
            }
            
            
            self.roi_result_label.setText(f"neutral x:{x}, y:{y}, w:{w}, h:{h}")

    def update_frame(self, frame):

        self.current_frame = frame.copy()   # 保存最新一张

        if not self.drawing_mode:
            DisplayBGR2RGB(frame, self.roi_img)
            

    def closeEvent(self, event):

        try:
            signal_bus.frame_ready.disconnect(self.update_frame)
        except TypeError:
            pass

        super().closeEvent(event)


class RoiImageLabel(QLabel):

    def __init__(self):
        super().__init__()

        self.start_point = None
        self.end_point = None

    def paintEvent(self,event):

        super().paintEvent(event)

        if self.start_point and self.end_point:

            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)

            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine) )

            painter.drawRect(QRect( self.start_point, self.end_point).normalized())
        
    def mousePressEvent(self, event):

        self.drawing = True

        self.start_point = event.pos()
        self.end_point = event.pos()

        self.update()

        super().mousePressEvent(event) 

    def mouseMoveEvent(self, event):

        if self.start_point is not None:

            if self.drawing:

                self.end_point = event.pos()

                self.update()

                super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):

        self.end_point = event.pos()

        self.drawing = False

        self.update()

        rect = QRect(self.start_point,self.end_point ).normalized()

   
        signal_bus.roi_position_setup.emit(rect.x(),rect.y(),rect.width(),rect.height())

        # print(
        #     rect.x(),
        #     rect.y(),
        #     rect.width(),
        #     rect.height()
        # )

        super().mouseReleaseEvent(event)


    def closeEvent(self, event):

        if self.camera_thread is not None:
            self.camera_thread.pause_emit = False

        self.drawing_mode = False
        self.clear_image()

        self.roi_img.setMouseTracking(False)
        self.roi_img.unsetCursor()

        event.accept()


