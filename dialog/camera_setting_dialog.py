from PySide6.QtWidgets import QDialog,QLabel, QHBoxLayout,QSlider,QRadioButton,QVBoxLayout,QGroupBox,QDialogButtonBox,\
                            QButtonGroup
from PySide6.QtCore import Qt

from style.css_style import MyCSS
from utils.config import config_manager

class CameraSettingDialog(QDialog):

    
    def __init__(self, parent=None): 
        super().__init__(parent) 

        # 保存相机参数配置的对象

         # 视窗标题
        self.setWindowTitle("Camera Setting")
        self.setFixedSize(500, 550)

        self.main_layout            = QVBoxLayout()
        self.radio_exposure_layout  = QHBoxLayout()
        self.radio_auto_white_balance_layout = QHBoxLayout()
        self.img_orientation_layout = QHBoxLayout()
        self.button_layout          = QHBoxLayout()
        self.expourse_group         = QButtonGroup(self)
        self.auto_white_balance_group = QButtonGroup(self)
        self.flip_group             = QButtonGroup(self)


        self.manual_mode = QRadioButton("Manual Mode")
        self.auto_mode = QRadioButton("Auto Mode")

        self.radio_exposure_layout.addWidget(self.manual_mode)
        self.radio_exposure_layout.addWidget(self.auto_mode)

        self.auto_white_balance_on = QRadioButton("On")
        self.auto_white_balance_off = QRadioButton("Off")
        self.radio_auto_white_balance_layout.addWidget(self.auto_white_balance_on)
        self.radio_auto_white_balance_layout.addWidget(self.auto_white_balance_off)


        self.manual_auto_box = QGroupBox("Auto Exposure")
        self.manual_auto_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        self.manual_auto_box.setLayout(self.radio_exposure_layout)

        self.auto_white_balance_box = QGroupBox("Auto White Blance")
        self.auto_white_balance_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        self.auto_white_balance_box.setLayout(self.radio_auto_white_balance_layout)


        self.v_flip_mode = QRadioButton("Vertical Flip")
        self.h_flip_mode = QRadioButton("Horizontal Flip")
        self.both_flip_mode = QRadioButton("Both Flips")

        self.img_orientation_layout.addWidget(self.h_flip_mode)
        self.img_orientation_layout.addWidget(self.v_flip_mode)
        self.img_orientation_layout.addWidget(self.both_flip_mode)

        self.flip_group_box = QGroupBox("Image Orientation")
        self.flip_group_box.setStyleSheet(MyCSS.GROUP_BOX_STYLE)
        self.flip_group_box.setLayout(self.img_orientation_layout)


        self.exposure_label,self.exposure_slider =\
        self.create_slider("Exposure Time",1,5000,config_manager.exposure)

        self.brightness_label, self.brightness_slider = \
        self.create_slider("Brightness",-128,127,config_manager.brightness)

        self.saturation_label, self.saturation_slider = \
        self.create_slider("Saturation",0,128,config_manager.saturation)

        self.contrast_label, self.contrast_slider = \
        self.create_slider("Contrast",0,64,config_manager.contrast)

        self.gamma_label, self.gamma_slider = \
        self.create_slider("Gamma",1,500,config_manager.gamma)

        self.white_balance_temperature_label, self.white_balance_temperature_slider = \
        self.create_slider("White Balance Temperature",2800,6500,config_manager.white_balance_temperature)

        self.sharpness_label, self.sharpness_slider = \
        self.create_slider("Sharpness",0,15,config_manager.sharpness)


        self.button_box = QDialogButtonBox(QDialogButtonBox.Save |QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.save_button_clicked)
        self.button_box.rejected.connect(self.reject)
        self.button_layout.addWidget(self.button_box)



      
        self.main_layout.addWidget(self.manual_auto_box)
        self.main_layout.addWidget(self.auto_white_balance_box )
        self.main_layout.addWidget(self.flip_group_box)
        self.main_layout.addWidget(self.exposure_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.exposure_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.brightness_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.brightness_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.saturation_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.saturation_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.contrast_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.contrast_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.gamma_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.gamma_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.white_balance_temperature_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.white_balance_temperature_slider,alignment= Qt.AlignLeft |Qt.AlignTop)

        self.main_layout.addWidget(self.sharpness_label,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addWidget(self.sharpness_slider,alignment= Qt.AlignLeft |Qt.AlignTop)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)



        self.expourse_group.addButton(self.manual_mode, 1)
        self.expourse_group.addButton(self.auto_mode, 3)
        expourse_button = self.expourse_group.button(config_manager.auto_exposure)

        self.auto_white_balance_group.addButton(self.auto_white_balance_on, 1)
        self.auto_white_balance_group.addButton(self.auto_white_balance_off, 0)
        auto_white_balance_button = self.auto_white_balance_group.button(config_manager.auto_white_balance)
        
        if expourse_button:
            expourse_button.setChecked(True)

        if auto_white_balance_button:
            auto_white_balance_button.setChecked(True)

        self.flip_group.addButton(self.v_flip_mode, 0)
        self.flip_group.addButton(self.h_flip_mode, 1)
        self.flip_group.addButton(self.both_flip_mode, -1)

        orientation_button = self.flip_group.button(config_manager.camera_flip)

        if orientation_button:
            orientation_button.setChecked(True) 
     

        self.setLayout(self.main_layout)


    def create_slider(self,text,min_value,max_value,default_value):  
          
          label = QLabel(f"{text} : {default_value}")
          slider = QSlider(Qt.Horizontal)
          slider.setFixedWidth(450)
          slider.setRange(min_value, max_value)
          slider.setValue(default_value)
          slider.valueChanged.connect(lambda value:label.setText(f"{text} : {value}"))

          return label, slider
    
    def save_button_clicked(self):
        

        config_manager.auto_exposure = (self.expourse_group.checkedId())
        config_manager.auto_white_balance = (self.auto_white_balance_group.checkedId())

        config_manager.camera_flip = (self.flip_group.checkedId())


        config_manager.exposure = \
            self.exposure_slider.value()

        config_manager.brightness = \
            self.brightness_slider.value()

        config_manager.saturation = \
            self.saturation_slider.value()

        config_manager.contrast = \
            self.contrast_slider.value()

        config_manager.gamma = \
            self.gamma_slider.value()

        config_manager.white_balance_temperature = \
            self.white_balance_temperature_slider.value()

        config_manager.sharpness = \
            self.sharpness_slider.value()

        config_manager.save_config()

        self.accept()

   

   