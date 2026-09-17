from utils.config import config_manager

class TerminalInspection(object):


    def __init__(self):

        config_manager.load_config()

        self.ground_roi = {"name": "ground",**config_manager.ground_roi}

        self.live_roi = {"name": "live",**config_manager.live_roi}

        self.neutral_roi = {"name": "neutral",**config_manager.neutral_roi}

        self.roi_configs = [self.ground_roi,self.live_roi,self.neutral_roi ]

    # for debug use
    @property
    def debug(self):
        return config_manager.debug
    
    @property
    def pixel_to_mm(self):
        return config_manager.calibration["width_pixel"] / config_manager.calibration["width_mm"]