from PySide6.QtGui import QFont,Qt
from PySide6.QtWidgets import QLabel,QPushButton,QHBoxLayout,QButtonGroup,QRadioButton,QGroupBox

from style.css_style import MyCSS

class AppStyle :

    def create_label_title(self,title,parent,x):

            label= QLabel(title,parent)
            label.move(x,6)
            label.setAlignment(Qt.AlignLeft)
            label.setFont(self.arial_font(True,True,15))
            label.setStyleSheet("""
                                border: 2px solid lightgray;
                                border-radius: 8px;
                                background-color: #D50000;
                                color : white
                                """)
            return label

    def create_label_valve(self,title,parent,x):

        label= QLabel(title,parent)
        label.move(x,8)
        label.setFixedWidth(115)
        label.setAlignment(Qt.AlignLeft)
        label.setFont(self.arial_font(False,True,15))
        label.setStyleSheet("""
                            background-color: #111;
                            color : white
                                """)    

        return label

    def create_button(self,title,parent,font_color,background,x):

        button = QPushButton(title,parent)
        button.setFixedSize(120,30)
        button.move(x,8)
        button.setFont(self.arial_font(True,False,15))
        button.setStyleSheet(f"""
                                color: {font_color};
                                background-color: {background};
                                border: 2px solid lighgreen;
                                border-radius: 8px;
                                """
                            )

        return button


    def create_dual_radio(self, radio1_text, radio2_text,
                    group_name, id1, id2):

        layout = QHBoxLayout()
        group_box = QGroupBox(group_name)
        button_group = QButtonGroup()

        radio1 = QRadioButton(radio1_text)
        radio2 = QRadioButton(radio2_text)

        layout.addWidget(radio1)
        layout.addStretch()
        layout.addWidget(radio2)
        group_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        group_box.setLayout(layout)

        button_group.addButton(radio1, id1)
        button_group.addButton(radio2, id2)

        return group_box, button_group,