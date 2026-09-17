
class MyCSS:

    MainCSS = """
                QMainWindow#MainBackGround{
                background-color: #121212; /* 炭黑 */
                border: 1px solid #333; /* 边框用更浅的灰 */
                margin: 0;}
                """
    MainMenuBar = """
                    QMenuBar {
                        background: #2b2b2b; /* 背景深灰黑 */
                        color: #e0e0e0;      /* 文字浅灰 */
                        border: none;
                        padding: 4px 0px;    /* 上下留点空 */
                        font-size: 13px;
                    }
                    
                    QMenuBar::item {
                        background: transparent;
                        padding: 6px 12px;
                        border-radius: 4px;
                        margin: 0px 2px;
                    }
                    
                    QMenuBar::item:selected { /* 悬停/点击 */
                        background: #3a3a3a; 
                        color: #ffffff;
                    }
                    
                    QMenu { /* 下拉菜单 */
                        background: #2b2b2b;
                        color: #e0e0e0;
                        border: 1px solid #444;
                        border-radius: 6px;
                    }
                    
                    QMenu::item:selected { /* 下拉菜单选中 */
                        background: #0078d4;
                        color: #ffffff;
                    }
                    """
    AboutUs = """
                QDialog {
                    background: #1a1a1a; /* 炭黑背景 */
                    border: 1px solid #333;
                    border-radius: 8px;
                }

                /* 自定义标题栏 */
                QLabel#titleLabel {
                    color: #e0e0e0;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "Segoe UI";
                }
                QPushButton#closeBtn {
                    background: transparent;
                    color: #e0e0e0;
                    border: none;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton#closeBtn:hover {
                    background: #e81123; /* 红色关闭 */
                    color: white;
                }

                /* 内容3个框 */
                QFrame#contentFrame {
                    background: #222;
                    border: 1px solid #333;
                    border-radius: 6px;
                    padding: 8px;
                }
                QLabel#companyName {
                    background: #2b2b2b;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    padding: 8px;
                    color: #00aaff; /* 蓝色高亮 */
                    font-size: 20px;
                    font-weight: bold;
                }
                QLabel#normalLabel {
                    background: #2b2b2b;
                    border: 1px solid #3a3a3a;
                    border-radius: 4px;
                    padding: 8px;
                    color: #e0e0e0;
                    font-size: 13px;
                }

                /* OK按钮 */
                QPushButton {
                    background: #0078d4; /* 你截图里的蓝色 */
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 24px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background: #0099ff;
                }
                """
    GROUP_BOX_STYLE = """
                QGroupBox {
                    border: 2px solid #ddd;
                    border-radius: 8px;
                    margin-top: 12px;
                    background: #fafafa;
                }

                QGroupBox::title {
                    color: #555;
                    font-weight: bold;
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }
                """
    
    LEFT_PANEL_STYLE = """
        #LeftButtonPanel {
            background: qlineargradient(x1:0 y1:0, x2:0 y2:1, 
                stop:0 #2193b0, stop:1 #6dd5ed);
            border-right: 2px solid #1565C0;    
        }

        #LeftButtonPanel QPushButton {
            background-color: #E1F5FE;      /* 亮蓝底 */
            color: #01579B;                 /* 深蓝字 */
            border: 2px solid #0288D1;      /* 边框 */
            border-radius: 8px;             /* 圆角 */
            padding: 5px;
            min-width: 140px;
            min-height: 30px;
        }
        #LeftButtonPanel QPushButton:hover {
            background-color: #B3E5FC;      /* 悬停变亮 */
            border: 2px solid #29B6F6;
        }
        #LeftButtonPanel QPushButton:pressed {
            background-color: #81D4FA;      /* 按下变深 */
            padding-top: 7px;               
        }

        /* 单独的Start按钮 - 绿色 */
        #LeftButtonPanel #StartButton {
            background-color: #C8E6C9;      /* 淡绿底 */
            color: #1B5E20;                 /* 深绿字 */
            border: 2px solid #66BB6A;
        }
        #LeftButtonPanel #StartButton:hover {
            background-color: #A5D6A7;
        }
        #LeftButtonPanel #StartButton:pressed {
            background-color: #81C784; 
            padding-top: 7px;
        }
        /* 单独的Stop按钮 */
        #LeftButtonPanel #StopButton {
            background-color: #FFCDD2;      /* 淡红底 */
            color: #B71C1C;                 /* 深红字 */
            border: 2px solid #E57373;
        }
        #LeftButtonPanel #StopButton:hover {  /*  */
        background-color: #EF9A9A;
        }
        #LeftButtonPanel #StopButton:pressed { /* */
            background-color: #E57373; 
            padding-top: 7px;
        }
        """
    GROUP_BOX_STYLE = """
                        QGroupBox {
                            border: 2px solid #ddd;
                            border-radius: 8px;
                            margin-top: 12px;
                            background: #fafafa;
                        }

                        QGroupBox::title {
                            color: #555;
                            font-weight: bold;
                            subcontrol-origin: margin;
                            left: 10px;
                            padding: 0 5px;
                        }
                        """
