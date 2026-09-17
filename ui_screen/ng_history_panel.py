from PySide6.QtWidgets import QVBoxLayout,QWidget,QLabel,QListWidget
from PySide6.QtCore import QTime
from style.font_style_manager import FontStyle


class NgHistoryRecord(QWidget):

    def __init__(self,main_window):

        super().__init__()

        self.main_window = main_window
        self.setFixedSize(500,295)

    def initialize(self):

        self.history_ng_record_layout = QVBoxLayout(self)

        self.ng_label = QLabel("Last 8 NG Records")
        self.ng_label.setFont(FontStyle.arial_font(True,False,10))
        self.ng_label.setStyleSheet("color: white; background-color: #0078FF; border: 2px solid #0078FF;")


        self.ng_list = QListWidget()
        self.ng_list.setFont(FontStyle.arial_font(False,False,14))
        self.ng_list.setStyleSheet("""
            QListWidget {
                background-color: black; 
                color: red; /* NG用红色 */
                border: 1px solid #0078FF;
            }
            QListWidget::item { padding: 3px; }
        """)
        self.ng_list.setMaximumHeight(295) # 固定5行高度

        self.history_ng_record_layout.addWidget(self.ng_label)
        self.history_ng_record_layout.addWidget(self.ng_list)

    def add_ng_log(self, pin_name, reason):

        time_str = QTime.currentTime().toString("HH:mm:ss :")
        log_text = f"{time_str}  {pin_name}  {reason}"
        
        self.ng_list.insertItem(0, log_text) # 插到最上面
        
        if self.ng_list.count() > 8: # 超过5条就删最老的
            self.ng_list.takeItem(8)
        
        self.ng_list.scrollToTop() # 自动滚到最上面