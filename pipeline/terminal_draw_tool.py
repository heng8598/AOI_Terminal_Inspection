import cv2 as cv
import numpy as np
from pipeline.base_inspection import TerminalInspection

class DrawTool(TerminalInspection):

    def __init__(self):

        super().__init__()

    def live_view_roi(self,frame):
        

        for roi in self.roi_configs:

            name = roi["name"]
            x = roi["x"]
            y = roi["y"]
            w = roi["w"]
            h = roi["h"] 

            (text_w, text_h), baseline = cv.getTextSize(name,cv.FONT_HERSHEY_SIMPLEX,0.8,1)

            cv.rectangle(frame,(x,y),(x + w, y + h ),(0,255,0),2,cv.LINE_8) 

            (text_w, text_h), baseline = cv.getTextSize(name,cv.FONT_HERSHEY_SIMPLEX,0.8,1)

            text_x = x + (w - text_w) // 2
            text_y = y + h + text_h -30
            
            cv.putText(frame,name,(text_x , text_y ),cv.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),1,cv.LINE_8)

    def level_line(self,frame):

        h, w = frame.shape[:2]
        cx = w // 2
        cy = h // 2
         # 水平线
        cv.line(frame, (0, cy), (w , cy), (0,0,255), 2)
        # 垂直线
        cv.line(frame, (cx, 0 ), (cx, h ), (0,0,255), 2) 

            

    def draw_result(self,img,termianl):

        module_name ="draw_result"

        name = termianl["name"]
        
        offset_x = termianl["offset_x"]
        offset_y = termianl["offset_y"]

        left_pin_top = termianl["width_termianl"]["left"]["left_top"]
        left_x = termianl["width_termianl"]["left"]["left_x"]
        left_y = termianl["width_termianl"]["left"]["left_y"]

        right_pin_top = termianl["width_termianl"]["right"]["right_top"]
        right_x = termianl["width_termianl"]["right"]["right_x"]
        right_y = termianl["width_termianl"]["right"]["right_y"]
        
        box_left = termianl["width_termianl"]["left"]["box_left"]
        box_right = termianl["width_termianl"]["right"]["box_right"]

        status_width = termianl["width_termianl"]["status_width"]
        status_angle = termianl["angle_terminal"]["status_angle"]
        pin_width = termianl["width_termianl"]["width_text"]


        if status_angle =="OK" and status_width == "OK" :

            color = (0,255,0)
           
        else:
            color = (0,0,255)
            
        left_center = (int(left_pin_top[0] + offset_x), int(left_pin_top[1] + offset_y))
        
        right_center = (int(right_pin_top[0] + offset_x),int(right_pin_top[1] + offset_y))

        cv.circle(img, left_center, 5, (255,0,0), -1)
        cv.circle(img, right_center, 5, (255,0,0), -1)
        cv.line(img, left_center, right_center, color, 2)

        cv.drawContours(img, [box_left],  0, color, 2,  offset=(offset_x + left_x, offset_y + left_y))
        
        cv.drawContours(img, [box_right],  0,  color,  2,   offset=(offset_x + right_x, offset_y + right_y))

        
        cv.putText(img,f"{name} : {pin_width} ",( offset_x - 40 , offset_y + 150),cv.FONT_HERSHEY_SIMPLEX,0.8,color,1,cv.LINE_8)

        return {
                "module": module_name,
                "status": "OK",
                "status_angle":status_angle,
                "status_width":status_width,
                "termianl_name":name,
                "img": img
            }     
        

