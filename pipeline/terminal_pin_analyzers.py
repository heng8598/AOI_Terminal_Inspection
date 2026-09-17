import cv2 as cv
import numpy as np
from pipeline.base_inspection import TerminalInspection
from utils.config import config_manager

class FindPinAPinB(TerminalInspection):

    def __init__(self):

        super().__init__()
        
    # 检查是否为二值图（0 和 255）    
    def is_binary(self, img):
        if img is None:
            return False
        return np.all((img == 0) | (img == 255))

    
    def find_pinA_pinB(self,img,x,y,w,h,name):

        parameter = getattr(config_manager,f"{name}_parameter")
    
        new_h = int(h * parameter["scan_height"])   
        new_y = y                 
        half = w // 2             

        match name :

            case "ground":
                left_x = x                
                left_y = new_y            
                left_w = half + 20           
                left_h = new_h     

                right_x = x + half        
                right_y = new_y           
                right_w = half + 20
                right_h = new_h  
   
            case "live":
                left_x = x                
                left_y = new_y            
                left_w = half + 30           
                left_h = new_h     

                right_x = x + half        
                right_y = new_y           
                right_w = half + 30 
                right_h = new_h  
            case "neutral":
                left_x = x                
                left_y = new_y            
                left_w = half + 30           
                left_h = new_h     

                right_x = x + half        
                right_y = new_y           
                right_w = half + 30
                right_h = new_h  
            case _:
              
                pass                           

        left_roi = img[left_y : left_y + left_h, left_x : left_x + left_w]  
        
        right_roi = img[right_y : right_y + right_h, right_x : right_x + right_w] 

        # cv.imshow("left roi",left_roi)
        # cv.imshow("right roi", right_roi)
        # print(left_roi.shape)
        # print(right_roi.shape)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        left_contour = cv.findContours(left_roi,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        valid_left_contour = [cnt for cnt in left_contour if cv.contourArea (cnt) > parameter["min_area"]]  


        # for i, cnt in enumerate(left_contour):
        #     area = cv.contourArea(cnt)
        #     print(f" Pin A {i, area}")

        if not valid_left_contour:

            pin_a = None
            
        else:    
            # 有 Pin A
            pin_a = max(valid_left_contour, key= cv.contourArea)

        # later add in debug
        if self.debug["find_pin"]:
            for i, cnt in enumerate(valid_left_contour):
                color = (0,255,0) if i == 0 else (0,0,255)
                draw_img = img.copy()
                draw_img = cv.cvtColor(draw_img, cv.COLOR_GRAY2BGR)
                cv.drawContours(draw_img, [cnt], -1, color, 2,offset=(left_x,left_y))
                cv.imshow("valid_left_contour",draw_img)
                cv.waitKey(0)
                cv.destroyAllWindows()


        right_contour = cv.findContours(right_roi,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        valid_right_contour = [cnt for cnt in right_contour if cv.contourArea (cnt) > parameter["min_area"]] 

        # print("right contour number:", len(right_contour))
        
        # for i, cnt in enumerate(right_contour):
        #     area = cv.contourArea(cnt)
        #     print(f" Pin B {i ,area}")

        if  not valid_right_contour:
            # 没有 Pin B
            pin_b = None
        else:    
            # 有 Pin B
            pin_b = max(valid_right_contour, key= cv.contourArea)

        # later add in debug
        if self.debug["find_pin"]:
            for i, cnt in enumerate(valid_right_contour):
                color = (0,255,0) if i == 0 else (0,0,255)
                draw_img = img.copy()
                draw_img = cv.cvtColor(draw_img, cv.COLOR_GRAY2BGR)
                cv.drawContours(draw_img, [cnt], -1, color, 2,offset=(right_x,right_y))
                cv.imshow("valid_right_contour",draw_img)
                cv.waitKey(0)
                cv.destroyAllWindows()
       
        return{
            "left":{
                    "left_roi":[left_y,left_h,left_x,left_w],
                    "left_contours":pin_a,
                    "left_x": left_x,
                    "left_y": left_y,
                    },
            "right":{
                    "right_roi":[right_y,right_h,right_x,right_w],
                    "right_contours":pin_b,
                    "right_x":right_x,
                    "right_y":right_y   
                    },    
            "pin": {
                    "A": 0 if pin_a is None else 1,
                    "B": 0 if pin_b is None else 1,
                    },
            "status": "OK",        
        }        