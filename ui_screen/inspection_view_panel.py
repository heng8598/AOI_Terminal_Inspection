from PySide6.QtWidgets import QWidget,QLabel,QVBoxLayout
from PySide6.QtCore import Qt

from style.font_style_manager import FontStyle
from utils.image_utils import DisplayBGR2RGB


class InspectionViewPanel(QWidget):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setStyleSheet("background-color: #2D2D2D; border: 2px solid #555; border-radius: 5px;")


    def initialize(self):

        self.inspection_view_title_label = QLabel("Inspection View")
        self.inspection_view_title_label.setFixedSize(645,50)
        self.inspection_view_title_label.setAlignment(Qt.AlignCenter)
        self.inspection_view_title_label.setFont(FontStyle.arial_font(True,False,20))
        self.inspection_view_title_label.setStyleSheet("""
                                                color: #AAAAAA;
                                                background-color: #3A3A3A;
                                                padding: 5px;
                                                border: 2px solid #1976D2;
                                                """)

        self.inspection_view_display_show = QLabel("No Signal")
        self.inspection_view_display_show.setFixedSize(645, 485)
        self.inspection_view_display_show.setAlignment(Qt.AlignCenter)
        self.inspection_view_display_show.setFont(FontStyle.arial_font(True,False,20))
        self.inspection_view_display_show.setStyleSheet("""
                                                color: #AAAAAA;
                                                background-color: #000;
                                                border: 2px solid #1976D2;
                                                    """)

        inspection_view_layout = QVBoxLayout(self)
        inspection_view_layout.addWidget(self.inspection_view_title_label)
        inspection_view_layout.addWidget(self.inspection_view_display_show)
        inspection_view_layout.addStretch()

    def update_frame(self,frame):

        if frame is None :
            self.inspection_view_display_show.setText("No Signal")
            self.inspection_view_display_show.setStyleSheet("background : red; color : white")
            return
        
        DisplayBGR2RGB(frame,self.inspection_view_display_show)    
        self.inspection_view_display_show.setText("") 
        self.inspection_view_title_label.setStyleSheet("background-color: #04EC65; color : blue") 
        self.inspection_view_display_show.setStyleSheet("background-color: #04EC65;") 
        self.inspection_view_title_label.setText("Inspection View - Running") 

    def inspection_stop_label(self):
        self.inspection_view_title_label.setStyleSheet("background : red; color : white")
        self.inspection_view_title_label.setText("Inspection View - Stop") 


