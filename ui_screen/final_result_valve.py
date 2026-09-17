from PySide6.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QHBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from style.font_style_manager import FontStyle
from utils.config import config_manager



class FinalResultValveTable(QWidget):

    def __init__(self,main_window):

        self.TABLE_ROW = 6
        self.TABLE_COL = 4
        super().__init__()

        self.main_window = main_window
        # self.setStyleSheet("background-color: lightbule; ")
        self.setFixedSize(620, 295)


    def initialize(self):
        
        self.final_table_layout = QHBoxLayout(self)
       
        self.final_table = QTableWidget(self.TABLE_ROW, self.TABLE_COL)
        self.final_table.verticalHeader().setVisible(False)
        self.final_table.horizontalHeader().setVisible(False)

        col_font = FontStyle.arial_font(True, False, 18) 
        row_font = FontStyle.arial_font(False, False, 16) 
        

        self.final_table.setRowHeight(0, 50)

        for i in range(1,self.TABLE_ROW ):
            self.final_table.setRowHeight(i, 40)

        for i in range(4):
            self.final_table.setColumnWidth(i,150)
         
       

        headers = ["Status", "Grounding", "Live", "Neutral"] # 第0列空
        for col, text in enumerate(headers):
            item = QTableWidgetItem(text)
            item.setFont(col_font)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(220, 220, 220))
            self.final_table.setItem(0, col, item)

        status = ["Pin A ", "Pin B", "Pin Width", "Pin Angle", "Pin Status"]
        for row, text in enumerate(status,start=1):
            item = QTableWidgetItem(text)
            item.setFont(row_font)
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QColor(220, 220, 220))
            self.final_table.setItem(row,0,item)  
            


        self.final_table_layout.addWidget(self.final_table)
     

    def update_pin_result(self,grounding_data, live_data,neutral_data):
        all_data =[grounding_data,live_data,neutral_data]
        result_font = FontStyle.arial_font(False,False,15)

        for col in range(3):

            # 根据 Column 选择规格
            if col == 0:
                parameter = config_manager.ground_parameter
            elif col == 1:
                parameter = config_manager.live_parameter
            else:
                parameter = config_manager.neutral_parameter

            for row in range(5):

                value = all_data[col][row]

                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(result_font)

                # --------------------
                # Row0 Pin A
                # --------------------
                if row == 0:

                    if value == "-":
                        pass

                    elif value == "OK":
                        item.setBackground(QColor(0,255,0))

                    elif value == "NG":
                        item.setBackground(QColor(255,0,0))

                # --------------------
                # Row1 Pin B
                # --------------------
                elif row == 1:

                    if value == "-":
                        pass
                    
                    elif value == "OK":
                        item.setBackground(QColor(0,255,0))

                    elif value == "NG":
                        item.setBackground(QColor(255,0,0))
                # --------------------
                # Row2 Width
                # --------------------
                elif row == 2:

                    try:

                        width = float(value.replace(" mm",""))

                        if width < parameter["width_min"] or width > parameter["width_max"]:
                            item.setBackground(QColor(255,0,0))
   
                    except ValueError:
                        pass        

                # --------------------
                # Row3 Angle
                # --------------------
                elif row == 3:

                    try:
                        angle = float(value.replace("°",""))

                        if angle < parameter["angle_min"] or angle > parameter["angle_max"]:
                            item.setBackground(QColor(255,0,0))


                    except ValueError:
                                            pass    
                # --------------------
                # Row4 Final
                # --------------------
                elif row == 4:

                    if value == "-":
                        pass
                    elif value == "OK":
                        item.setBackground(QColor(0,255,0))

                    elif value == "NG":
                        item.setBackground(QColor(255,0,0))

                self.final_table.setItem(row+1, col+1, item)

            