from PySide6.QtWidgets import QDialog,QGroupBox, QHBoxLayout,QRadioButton,QButtonGroup,QMessageBox,\
                                QLineEdit,QVBoxLayout,QLabel,QFormLayout,QDialogButtonBox

from style.css_style import MyCSS
from utils.config import config_manager

class DetectionParameters(QDialog):

    def __init__(self,parent=None):

        super().__init__(parent) 
        self.setWindowTitle("Detection Parameters")
        self.setFixedSize(500, 350)

        self.main_layout                = QVBoxLayout()
        self.detection_parameters_layout = QHBoxLayout()
        self.form = QFormLayout()
        self.button_layout = QHBoxLayout()

        self.radio_ground_parameter = QRadioButton("Ground Parameters")
        self.radio_ground_parameter.setChecked(True)

        self.radio_live_parameters = QRadioButton("Live Parameters")
        self.radio_neutral_parameters = QRadioButton("Neutral Parameters")

        self.detection_parameters_layout.addWidget(self.radio_ground_parameter)
        self.detection_parameters_layout.addWidget(self.radio_live_parameters)
        self.detection_parameters_layout.addWidget(self.radio_neutral_parameters)

        self.detection_parameter_box = QGroupBox("Detection parameter")
        self.detection_parameter_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        self.detection_parameter_box.setLayout(self.detection_parameters_layout)

        terminal = config_manager.ground_parameter
        _, self.qline_width_min = self.create_qline("WIDTH MIN THRESHOLDS",str(terminal["width_min"]))
        _, self.qline_width_max = self.create_qline("WIDTH MAX THRESHOLDS", str(terminal["width_max"]))
        _, self.qline_angle_min = self.create_qline("ANGLE MIN THRESHOLDS", str(terminal["angle_min"]))
        _, self.qline_angle_max = self.create_qline("ANGLE MAX THRESHOLDS", str(terminal["angle_max"]))
        _, self.qline_scan_height_ratio = self.create_qline("SCAN HEIGHT RATIO ",str(terminal["scan_height"]))
        _, self.qline_pin_thickness = self.create_qline(" PIN THICKNESS ", str(terminal["pin_thickness"]))
        _, self.qline_min_area = self.create_qline("MIN AREA THRESHOLDS ", str(terminal["min_area"]))
         
      
        self.form.addRow("WIDTH_MIN_THRESHOLDS  :", self.qline_width_min)
        self.form.addRow("WIDTH MAX THRESHOLDS  :", self.qline_width_max )
        self.form.addRow("ANGLE MIN THRESHOLDS  :", self.qline_angle_min)
        self.form.addRow("ANGLE MAX THRESHOLDS  :", self.qline_angle_max)
        self.form.addRow("SCAN HEIGHT RATIO     :", self.qline_scan_height_ratio )
        self.form.addRow("PIN THICKNESS         :", self.qline_pin_thickness)
        self.form.addRow("MIN AREA THRESHOLDS   :", self.qline_min_area)
    
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save |QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.reject)
        self.button_layout.addWidget(self.button_box)
        
        self.main_layout.addWidget(self.detection_parameter_box)
        self.main_layout.addLayout(self.form)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)

        self.paratemert_group_button = QButtonGroup(self)
        self.paratemert_group_button.addButton(self.radio_ground_parameter,1)
        self.paratemert_group_button.addButton(self.radio_live_parameters,2)
        self.paratemert_group_button.addButton(self.radio_neutral_parameters,3)

        self.setLayout(self.main_layout)

        self.radio_ground_parameter.toggled.connect(
                lambda checked: checked and self.load_parameter("ground")
            )

        self.radio_live_parameters.toggled.connect(
                lambda checked: checked and self.load_parameter("live")
            )

        self.radio_neutral_parameters.toggled.connect(
                lambda checked: checked and self.load_parameter("neutral")
            )
        
        

    def save_button_clicked(self):

        terminal_map = {
        1: config_manager.ground_parameter,
        2: config_manager.live_parameter,
        3: config_manager.neutral_parameter,
        }

        terminal = terminal_map[self.paratemert_group_button.checkedId()]

        terminal["width_min"] = round(float(self.qline_width_min.text()),2)
        terminal["width_max"] = round(float(self.qline_width_max.text()),2)
        terminal["angle_min"] = round(float(self.qline_angle_min.text()),2)
        terminal["angle_max"] = round(float(self.qline_angle_max.text()),2)
        terminal["scan_height"] = round(float(self.qline_scan_height_ratio.text()),2)
        terminal["pin_thickness"] = round(float(self.qline_pin_thickness.text()),2)
        terminal["min_area"] = int(self.qline_min_area.text())

        config_manager.save_config()

        reply = QMessageBox.question(self,"Save Parameter",
                                            "parameter saved successfully.\n\nContinue editing Parameters?",
                                                QMessageBox.Yes | QMessageBox.No
                                            )

        if reply == QMessageBox.No:
                    
            self.accept()        



    def create_qline(self, text, default_value):

        label = QLabel(f"{text} :")
        qline_edit = QLineEdit(str(default_value))
        qline_edit.setFixedWidth(100)

        return label, qline_edit

    def load_parameter(self,parameter):

        if parameter == "ground":

            terminal = config_manager.ground_parameter

        elif parameter == "live":
            terminal = config_manager.live_parameter


        else:
            terminal = config_manager.neutral_parameter

        self.qline_width_min.setText(str(terminal["width_min"]))
        self.qline_width_max.setText(str(terminal["width_max"]))
        self.qline_angle_min.setText (str(terminal["angle_min"]))
        self.qline_angle_max.setText (str(terminal["angle_max"]))
        self.qline_scan_height_ratio.setText (str(terminal["scan_height"]))
        self.qline_pin_thickness.setText (str(terminal["pin_thickness"]))
        self.qline_min_area.setText (str(terminal["min_area"]))
            

