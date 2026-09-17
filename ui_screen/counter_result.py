from PySide6.QtWidgets import QHBoxLayout,QWidget,QLabel,QGridLayout,QSizePolicy
from PySide6.QtCore import Qt
from style.font_style_manager import FontStyle

class CounterResultLable(QWidget):

    def __init__(self, main_window,ok_count,ng_count,total_count):
        super().__init__()
        self.main_window = main_window
        self.ok_count = ok_count
        self.ng_count = ng_count
        self.total_count = total_count
        self.setStyleSheet("background-color: #0A1629;") # 深蓝背景
        self.setFixedSize(1350, 60)

    def initialize(self):
        self.counter_result_layout = QHBoxLayout(self)
        self.counter_result_layout.setContentsMargins(15, 5, 15, 5)
        self.counter_result_layout.setSpacing(15)

        title_font = FontStyle.arial_font(True, False, 15)
        value_font = FontStyle.arial_font(True, False, 20)

        self.check_counter_text_label = QLabel("Check Counter :")
        self.check_counter_value_label = QLabel("0")
        
        self.ok_counter_text_label = QLabel("OK Counter :")
        self.ok_counter_value_label = QLabel("0")
        
        self.ng_counter_text_label = QLabel("NG Counter :")
        self.ng_counter_value_label = QLabel("0")
        
        self.yield_text_label = QLabel("Yield :")
        self.yield_value_label = QLabel("0.00%")
        
        # 标题样式：深蓝底白字 蓝边
        title_style = """
            QLabel {
                color: white; 
                background-color: #1B2A4A; 
                padding: 4px 12px; 
                border: 2px solid #0078FF;
                border-radius: 4px;
                font-weight: bold;
            }
        """
        # 数值样式：黑底蓝字 蓝边发光
        value_style = """
            QLabel {
                color: #00BFFF; 
                background-color: #000000; 
                padding: 4px 12px; 
                border: 2px solid #0078FF;
                border-radius: 4px;
            }
        """
        
        for label in [self.check_counter_text_label, self.ok_counter_text_label, 
                      self.ng_counter_text_label, self.yield_text_label]:
            label.setFont(title_font)
            label.setStyleSheet(title_style)
            label.setAlignment(Qt.AlignCenter)
        
        for label in [self.check_counter_value_label, self.ok_counter_value_label, 
                      self.ng_counter_value_label, self.yield_value_label]:
            label.setFont(value_font)
            label.setStyleSheet(value_style)
            label.setAlignment(Qt.AlignCenter)
            label.setFixedWidth(150)
            label.setFixedHeight(40)
        
        # 加到一行
        self.counter_result_layout.addWidget(self.check_counter_text_label)
        self.counter_result_layout.addWidget(self.check_counter_value_label)
        self.counter_result_layout.addSpacing(10)
        
        self.counter_result_layout.addWidget(self.ok_counter_text_label)
        self.counter_result_layout.addWidget(self.ok_counter_value_label)
        self.counter_result_layout.addSpacing(10)
        
        self.counter_result_layout.addWidget(self.ng_counter_text_label)
        self.counter_result_layout.addWidget(self.ng_counter_value_label)
        self.counter_result_layout.addSpacing(10)
        
        self.counter_result_layout.addWidget(self.yield_text_label)
        self.counter_result_layout.addWidget(self.yield_value_label)
        
        self.counter_result_layout.addStretch()

       

    def update_check_counter(self, valve):
        self.check_counter_value_label.setText(str(valve))
        self.update_yield()

    def update_ok_counter(self, valve):
        self.ok_counter_value_label.setText(str(valve))
        self.update_yield()
        self.set_ok_color(valve)

    def update_ng_counter(self, valve):
        self.ng_counter_value_label.setText(str(valve))
        self.update_yield()
        self.set_ng_color(valve)

    def update_yield(self):

        check = self.total_count.get()
        ok = self.ok_count.get()
        
        yield_val = (ok / check * 100) if check > 0 else 0
        self.yield_value_label.setText(f"{yield_val:.2f}%")
     
    
    def set_ok_color(self, valve): # OK>0 蓝变绿
        if int(valve) > 0:
            self.ok_counter_value_label.setStyleSheet("color: #00FF7F; background-color: #000; padding: 4px 12px; border: 2px solid #00FF7F; border-radius: 4px;")
        else:
            self.ok_counter_value_label.setStyleSheet("color: #00BFFF; background-color: #000000; padding: 4px 12px; border: 2px solid #0078FF; border-radius: 4px;")
    
    def set_ng_color(self, valve): # NG>0 蓝变红
        if int(valve) > 0:
            self.ng_counter_value_label.setStyleSheet("color: #FF3B3B; background-color: #000000; padding: 4px 12px; border: 2px solid #FF3B3B; border-radius: 4px;")
        else:
            self.ng_counter_value_label.setStyleSheet("color: #00BFFF; background-color: #000000; padding: 4px 12px; border: 2px solid #0078FF; border-radius: 4px;")