import cv2 as cv
import numpy as np
from pipeline.base_inspection import TerminalInspection
from utils.config import config_manager

import math

class TerminalMeassurement(TerminalInspection):

    def __init__(self):
        super().__init__()

    def calculate_width(self,contour):

        module_name = "calculate_width"

        points = contour.squeeze()

        if len(points.shape) != 2 or len(points) < 10:
            return {
            "module": module_name,
            "status": "ERROR",
            "msg": f"contour error: {points.shape}",
            "img": None
        }
        sorted_pts = points[points[:, 1].argsort()]
        
        # 取顶部 10% 的点
        min_y = sorted_pts[0][1]
        max_y = sorted_pts[-1][1]
        height = max_y - min_y
        top_threshold = min_y + height * self.TOP_SAMPLING_RATIO
        top_points = sorted_pts[sorted_pts[:, 1] <= top_threshold]
        
        if len(top_points) < 5:

            return {
                "module": module_name,
                "status": "ERROR",
                "msg": f"top point: {len(top_points)}",
                "img": None
            }
        
        
        min_x = np.min(top_points[:, 0])
        max_x = np.max(top_points[:, 0])
        width_px = max_x - min_x
        width_mm = width_px /self.pixel_to_mm
        

        ys = np.unique(top_points[:,1])

        for y in ys:

            row = top_points[top_points[:,1] == y]

            w = np.max(row[:,0]) - np.min(row[:,0])

        #     print(y, w)
        # print(f"width px : {width_px}")

         # 成功返回
        return {
            "module": module_name,
            "status": "Ok",
            "msg": "calc width done",
            "img": width_mm   
        }
        
    def calculate_angle_terminal(self,name,left_contour, right_contour,left_x, left_y, right_x, right_y):
        
        module_name = "calculate_angle"

        parameter = getattr(config_manager,f"{name}_parameter")

        left_M = cv.moments(left_contour)

        left_cx = left_M["m10"] / left_M["m00"] + left_x
        left_cy = left_M["m01"] / left_M["m00"] + left_y

        right_M = cv.moments(right_contour) 

        right_cx = right_M["m10"] / right_M["m00"] + right_x
        right_cy = right_M["m01"] / right_M["m00"] + right_y

        # pt1 = (round(left_cx + offset_x), round(left_cy+offset_y))
        # pt2 = (round(right_cx +offset_x), round(right_cy + offset_y))

        dx = right_cx - left_cx
        dy = right_cy - left_cy

        # cv.line(img,pt1,pt2,(0,255,0),2)

        raw_angle = math.degrees(math.atan2(dy, dx))

        if parameter["angle_min"] <= raw_angle <= parameter["angle_max"] :
                 
            status_angle = "OK"
        else :   
            status_angle = "NG"    

        return {
            "module": module_name,
                "status": "Ok",
                "msg": "calc angle done",
                "status_angle":status_angle,
                "raw_angle":raw_angle,
                "angle_text":f"{raw_angle: .2f}°", 
            }
                                
    # def calculate_angle_terminal(self, name, left_contour, right_contour, left_x, left_y, right_x, right_y):
    #     """
    #     用 minAreaRect 计算引脚角度（稳定版）
    #     """
    #     module_name = "calculate_angle"
    #     parameter = getattr(config_manager, f"{name}_parameter")

    #     # 1. 用 minAreaRect 获取引脚的长轴方向
    #     rect_left = cv.minAreaRect(left_contour)
    #     rect_right = cv.minAreaRect(right_contour)

    #         # 2. 获取四个角点
    #     box_left = cv.boxPoints(rect_left)
    #     box_right = cv.boxPoints(rect_right)

    #     # 3. 取最上面两点（Y 最小的两点）
    #     top_left = box_left[np.argsort(box_left[:, 1])[:2]]
    #     top_right = box_right[np.argsort(box_right[:, 1])[:2]]

    #     # 4. 取平均
    #     left_top = np.mean(top_left, axis=0)
    #     right_top = np.mean(top_right, axis=0)

    #     # 5. 转换到全局坐标
    #     left_top[0] += left_x
    #     left_top[1] += left_y
    #     right_top[0] += right_x
    #     right_top[1] += right_y

    #     # 6. 计算角度
    #     dx = right_top[0] - left_top[0]
    #     dy = right_top[1] - left_top[1]

    #     raw_angle = np.degrees(np.arctan2(dy, dx))

    #     # 5. OK/NG 判定
    #     if parameter["angle_min"] <= raw_angle <= parameter["angle_max"]:
    #         status_angle = "OK"
    #     else:
    #         status_angle = "NG"

    #     return {
    #         "module": module_name,
    #         "status": "Ok",
    #         "msg": "calc angle done",
    #         "status_angle": status_angle,
    #         "raw_angle": raw_angle,
    #         "angle_text": f"{raw_angle:.2f}°",
    #     }
        

    def calculate_width_terminal(self,name,left_contour, right_contour, left_x, left_y, right_x, right_y):

        module_name = "calculate_width_width"

        parameter = getattr(config_manager,f"{name}_parameter")

        # Min Area Rect
        rect_left = cv.minAreaRect(left_contour)
        rect_right = cv.minAreaRect(right_contour)


        # 四個角
        box_left = cv.boxPoints(rect_left).astype(np.int32)
        box_right = cv.boxPoints(rect_right).astype(np.int32)
        # print(box_left)

        float_left = cv.boxPoints(rect_left).astype(np.float32)
        float_right = cv.boxPoints(rect_right).astype(np.float32)
        # print(float_left)
        # print(float_right)


        # -------------------------
        # Left Pin 最上面兩點
        # -------------------------
        
        top_left = box_left[np.argsort(box_left[:,1])[:2]]
        top_float_left = float_left[np.argsort(float_left[:,1])[:2]]
    
        # 左右排序
        top_left = top_left[np.argsort(top_left[:,0])]
        top_float_left = top_float_left[np.argsort(top_float_left[:,0])]
    
        # 左 Pin 的頂點
        left_pin_top = top_left.mean(axis=0)
        float_left_pin_top =top_float_left.mean(axis=0)
        # print(left_pin_top)

        # -------------------------
        # Right Pin 最上面兩點
        # -------------------------
        top_right = box_right[np.argsort(box_right[:,1])[:2]]
        top_float_right = float_right[np.argsort(float_right[:,1])[:2]]

        top_right = top_right[np.argsort(top_right[:,0])]
        top_float_right = top_float_right[np.argsort(top_float_right[:,0])]

        right_pin_top = top_right.mean(axis=0)
        float_right_pin_top = top_float_right.mean(axis=0)
    
    

        # ROI 座標 → 原圖座標
        for pin_top, float_pin_top, x_offset, y_offset in [
        (left_pin_top, float_left_pin_top, left_x, left_y),
        (right_pin_top, float_right_pin_top, right_x, right_y)]:
            pin_top[0] += x_offset
            pin_top[1] += y_offset
            float_pin_top[0] += x_offset
            float_pin_top[1] += y_offset


        dx = float_right_pin_top[0] - float_left_pin_top[0]
        dy = float_right_pin_top[1] - float_left_pin_top[1]

        if name == "ground":

            pixel_width = np.sqrt(dx**2 + dy**2) + 9

        else :
            pixel_width = np.sqrt(dx**2 + dy**2) + 11

        width_mm = pixel_width/self.pixel_to_mm # pin to pin center
                
        out_dimension = width_mm + parameter["pin_thickness"] 

        if parameter["width_min"] <= out_dimension <= parameter["width_max"]:
        
            status_width = "OK"
        else :   
            status_width = "NG" 

        # 計算角度
        # dx = right_pin_top[0] - left_pin_top[0]
        # dy = right_pin_top[1] - left_pin_top[1]

        # raw_angle = np.degrees(np.arctan2(dy, dx))


        # if parameter["angle_min"] <= raw_angle <= parameter["angle_max"] :
         
        #     status_angle = "OK"
        # else :   
        #     status_angle = "NG" 
      
            
        return {
            "module": module_name,
            "status": "Ok",
            "status_width":status_width,
            "width_pixel": pixel_width,
            "width_mm": out_dimension,      
            "width_text": f"{out_dimension:.2f} mm",
            "left":{
                "box_left":box_left,
                "left_top": left_pin_top,
                "left_x":left_x,
                "left_y":left_y,
            },
            "right":{
                "box_right":box_right,
                "right_top": right_pin_top,
                "right_x":right_x,
                "right_y":right_y,

            },
            
        }

   
        
    