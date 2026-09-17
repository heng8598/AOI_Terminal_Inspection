from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout
from PySide6.QtCore import Qt

from camera.signal_bus import signal_bus
from utils.config import config_manager

from style.font_style_manager import FontStyle
from utils.image_utils import DisplayBGR2RGB



class LiveViewPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #2D2D2D; border: 2px solid #555; border-radius: 5px;")


    def initialize(self):

        self.live_view_title_label = QLabel("Live View")
        self.live_view_title_label.setFixedSize(650,50)
        self.live_view_title_label.setAlignment(Qt.AlignCenter)
        self.live_view_title_label.setFont(FontStyle.arial_font(True,False,20))
        self.live_view_title_label.setStyleSheet("""
                                                color: #AAAAAA;
                                                background-color: #3A3A3A;
                                                padding: 5px;
                                                border: 2px solid #1976D2;
                                                """)

        self.live_view_display_show = QLabel("No Signal")
        self.live_view_display_show.setFixedSize(650, 490)
        self.live_view_display_show.setAlignment(Qt.AlignCenter)
        self.live_view_display_show.setFont(FontStyle.arial_font(True,False,20))
        self.live_view_display_show.setStyleSheet("""
                                                color: #AAAAAA;
                                                background-color: #000;
                                                border: 2px solid #1976D2;
                                                    """)

        live_view_layout = QVBoxLayout(self)
        live_view_layout.addWidget(self.live_view_title_label)
        live_view_layout.addWidget(self.live_view_display_show)
        live_view_layout.addStretch()

        signal_bus.camera_disconnected.connect(self.show_camera_error)

    def update_frame(self,frame):


        if frame is None :
            self.live_view_title_label.setText("Live View") 
            self.live_view_title_label.setStyleSheet("background-color: #3A3A3A;")
            self.live_view_display_show.setStyleSheet("background-color: #000;")
            return
        
        if config_manager.debug["live view"]:
            DisplayBGR2RGB(frame,self.live_view_display_show)    
            self.live_view_display_show.setText("") 
            self.live_view_title_label.setStyleSheet("background-color: #04EC65; color : blue") 
            self.live_view_display_show.setStyleSheet("background-color: #04EC65;") 
            self.live_view_title_label.setText("Live View - Running")     



    def show_camera_error(self):

        self.live_view_display_show.setText("No Signal")
        self.live_view_display_show.setStyleSheet("background:red;color:white")

        self.live_view_title_label.setText("Camera Error")
        self.live_view_title_label.setStyleSheet("background:red;color:white")