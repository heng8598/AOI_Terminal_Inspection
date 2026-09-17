import json
import os

CONFIG_FILE = "config.json"


class ConfigManager:

    def __init__(self, filepath="config.json"):

        self.filepath = filepath

        # Camera Setting default
        self.camera_index = 0
        self.camera_flip = 0
        self.auto_exposure = 1
        self.auto_white_balance = 0
        self.white_balance_temperature = 4000
        self.exposure = 200
        self.brightness = 0
        self.saturation = 32
        self.contrast = 32
        self.gamma = 100
        self.sharpness = 0
        self.ground_roi = {
            "x":230,
            "y":5,
            "w":450,
            "h":230
        }
        self.live_roi = {
            "x":90,
            "y":250,
            "w":330,
            "h":465
        }

        self.neutral_roi = {
            "x":370,
            "y":250,
            "w":610,
            "h":465
        }
        self.uart = {
            "baudrate":115200,
            "com_port":0
        }

        self.modbus_tcp = {
            "ip_address": "192.168.0.10",
            "port": 502,
            "subnet_mask" : "255.255.255.0",
            "slave_id": 1,
            "inspection_start" : 100,
            "product_leave": 300
        }
        self.comm_mode = {
            "manual":0,
            "auto":0,
            "uart":0,
            "modbus_tcp":0
        }
        self.debug ={
            "live view": False,
            "binary": False,
            "contour": False,
            "roi": False,
            "roi_image" : False,
            "find_pin": False,
            "image_health":False,
            "subpixel_image": False,
            "result": False
        }
        
        self.ground_parameter = {
            "width_min": 3.80,
            "width_max": 4.60,
            "angle_min": 5,
            "angle_max":-5,
            "scan_height": 0.20,
            "pin_thickness": 0.38,
            "largest_area":2000,
            "smaller_area" : 200,
            "min_area": 100,
        }

        self.live_parameter = {
            "width_min": 4.80,
            "width_max": 5.60,
            "angle_min": 5,
            "angle_max": -5,
            "scan_height": 0.35,
            "pin_thickness": 0.75,
            "largest_area":2000,
            "smaller_area" : 200,
            "min_area": 500,
        }

        self.neutral_parameter = {
            "width_min": 4.80,
            "width_max": 5.60,
            "angle_min": 5,
            "angle_max": -5,
            "scan_height": 0.35,
            "pin_thickness": 0.75,
            "largest_area":2000,
            "smaller_area" : 200,
            "min_area": 500,           
        }
        self.calibration = {
            "width_mm" : 5.2,
            "width_pixel" : 115,
        }
        self.image_tuning = {
            "gaussian_x":19,
            "gaussian_y":21
        }



    def save_config(self):

        config_data = {
            "camera_index": self.camera_index,
            "camera_flip":self.camera_flip,
            "auto_exposure": self.auto_exposure,
            "auto_white_balance":self.auto_white_balance,
            "exposure": self.exposure,
            "brightness": self.brightness,
            "saturation": self.saturation,
            "contrast": self.contrast,
            "gamma": self.gamma,
            "white_balance_temperature": self.white_balance_temperature,
            "ground_roi": self.ground_roi,
            "live_roi":self.live_roi,
            "neutral_roi":self.neutral_roi,
            "comm_mode":self.comm_mode,
            "uart":self.uart,
            "modbus_tcp":self.modbus_tcp,
            "debug":self.debug,
            "ground_parameter":self.ground_parameter,
            "live_parameter":self.live_parameter,
            "neutral_parameter":self.neutral_parameter,
            "calibration":self.calibration,
            "image_tunning":self.image_tuning,
        }

        with open(self.filepath, "w", encoding="utf-8") as file:

            json.dump(config_data, file,indent=4, ensure_ascii=False)

    def load_config(self):

        if not os.path.exists(self.filepath):
            return False

        with open(self.filepath, "r", encoding="utf-8") as file:

            config_data = json.load(file)

        for key, value in config_data.items():

            if hasattr(self, key):

                setattr(self, key, value)

        return True
    
config_manager = ConfigManager()   