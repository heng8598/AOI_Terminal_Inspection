from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
from PySide6.QtCore import Qt
from style.css_style import MyCSS

class AboutUsDialog(QDialog):

    def __init__(self, parent=None): 
        super().__init__(parent)     
        self.setWindowTitle("About Us")
        self.setFixedSize(650, 320) # 
        self.setStyleSheet(MyCSS.AboutUs)
        self.setWindowFlags(
            Qt.Dialog | 
            Qt.FramelessWindowHint | # 无边框
            Qt.Tool | # 不在任务栏显示
            Qt.WindowStaysOnTopHint # 置顶
        )
        self.setAttribute(Qt.WA_QuitOnClose, False)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        # 1. 自定义标题栏
        title_bar = QHBoxLayout()
        title_label = QLabel("About Us")
        title_label.setObjectName("titleLabel")
        btn_close = QPushButton("X")
        btn_close.setObjectName("closeBtn")
        btn_close.setFixedSize(24, 24)
        btn_close.clicked.connect(self.close)
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        title_bar.addWidget(btn_close)

        # 2. 内容区
        frame = QFrame()
        frame.setObjectName("contentFrame")
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(8)

        company = QLabel("PT. ZEN TRAINING ENGINEERING & KONSTRUKSI")
        company.setObjectName("companyName")
        company.setWordWrap(True) # 防止被截断
        
        system = QLabel("AOI Terminal Inspection System")
        system.setObjectName("normalLabel")
        
        version = QLabel("Version 1.0")
        version.setObjectName("normalLabel")

        frame_layout.addWidget(company)
        frame_layout.addWidget(system)
        frame_layout.addWidget(version)

        # 3. OK按钮
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)

        main_layout.addLayout(title_bar)
        main_layout.addWidget(frame)
        main_layout.addLayout(btn_layout)