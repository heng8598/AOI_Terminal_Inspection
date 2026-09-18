import cv2 as cv
import numpy as np

from pipeline.base_inspection import TerminalInspection
from pipeline.terminal_analyzers import TerminalAnalyzer
from pipeline.terminal_pin_analyzers import FindPinAPinB
from pipeline.terminal_measurement import TerminalMeassurement

from pipeline.terminal_draw_tool import DrawTool

import hashlib

terminal_inspection = TerminalInspection()
terminal_analyzer = TerminalAnalyzer()
find_pin = FindPinAPinB()
messsurement = TerminalMeassurement()
draw_img = DrawTool()


ground_width_list = []
ground_angle_list = []
live_width_list = []
live_angle_list = []
neutral_width_list = []
neutral_angle_list = []
frame_list = []
def check_frame(frame):

    md5 = hashlib.md5(frame.tobytes()).hexdigest()

    print(
        "id:",
        id(frame),
        "mean:",
        frame.mean(),
        "hash:",
        md5[:8]
    )

def prosess_inspection(frame):

    module_name = ("process inspection")

    if frame is None:
        return{"module": module_name,"status": "ERROR","msg": " img is None","img": None }
    
    bv_img = terminal_analyzer.preprocess_bv(frame)

    if bv_img.get("status") != "OK":

        return
    
    img = bv_img.get("img")

    result = [] 

    for roi in terminal_inspection.roi_configs:

        name = roi["name"]
        x, y, w, h = roi["x"], roi["y"], roi["w"], roi["h"]

        img_roi = img[y: y+h, x: x+w]

        binary_contour = terminal_analyzer.binary_terminal_contours(img_roi,name,)

        if binary_contour.get("status") != "OK":
         
            return {"module": "prosess_inspection","status": "ERROR","msg": binary_contour.get("msg", "Binary contour failed")}


        binary_img = binary_contour["img"]
        bx = binary_contour["bounding_x"] 
        by = binary_contour["bounding_y"]
        bw = binary_contour["bounding_w"]
        bh = binary_contour["bounding_h"]

        pin_result = find_pin.find_pinA_pinB(binary_img,bx,by,bw,bh,name)

        result.append({
                        "name":name,
                        "offset_x":roi["x"],
                        "offset_y":roi["y"],
                        "binary_contour":binary_contour,
                        "pin_result":pin_result,
                        "img":img_roi
                        })


    missing_list = []
    #  检查缺失
    for terminal in result:

        pin = terminal["pin_result"]["pin"]

        for pin_name, pin_leg in pin.items():

            if pin_leg != 1 :
                missing_list.append((terminal['name'],pin_name))
                

    if missing_list:

        img = frame.copy()

        offset_y = 100

        for name, pin in missing_list:

            cv.putText(img,f"Terminal {name} Pin {pin} Missing",(100, offset_y),cv.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),3)

            offset_y += 50

        inspection_data = {
        "module": module_name,
        "status": "ERROR",
        "msg": "Terminal Missing",
        "result": result,
        "missing": missing_list,
        "missing_img": img
        }


        return inspection_data

    img = frame.copy()

    for terminal in result:

        name = terminal["name"]
        offset_x = terminal["offset_x"]
        offset_y = terminal["offset_y"]
        left_contour = terminal["pin_result"]["left"]["left_contours"]
        left_x = terminal["pin_result"]["left"]["left_x"]
        left_y = terminal["pin_result"]["left"]["left_y"]
        left_box = terminal["pin_result"]["left"]["left_y"]

        right_contour = terminal["pin_result"]["right"]["right_contours"]
        right_x = terminal["pin_result"]["right"]["right_x"]
        right_y = terminal["pin_result"]["right"]["right_y"]
        # img_angle = terminal["img"]

        angle_terminal = messsurement.calculate_angle_terminal(name,left_contour,right_contour,left_x,left_y,right_x,right_y)
        terminal["angle_terminal"] = angle_terminal
                

        widht_terminal = messsurement.calculate_width_terminal(name,left_contour,right_contour,left_x,left_y,right_x,right_y)
        terminal["width_termianl"] = widht_terminal

        # left_box = widht_terminal["left"]["box_left"]
        # right_box = widht_terminal["right"]["box_right"]
        

        # angle_terminal = messsurement.calculate_angle_terminal(name,img_angle,left_box,right_box,left_x,left_y,right_x,right_y)
        # terminal["angle_terminal"] = angle_terminal
        

        # if name == "ground":

        #     angle_value = angle_terminal.get("raw_angle")
        #     width_value = widht_terminal.get("width_mm")

        #     ground_angle_list.append(angle_value)
        #     ground_width_list.append(width_value)

        #     count = len(ground_angle_list)

        #     if count in [100, 500, 1000, 1500, 2000,5000,100000,150000]:

        #         calculate_width_cpk(ground_width_list,name,4.19)
        #         calculate_angle_cpk(ground_angle_list,name,0)

        # if name == "live":
        
        #     angle_value = angle_terminal.get("raw_angle")
        #     width_value = widht_terminal.get("width_mm")

        #     live_angle_list.append(angle_value)
        #     live_width_list.append(width_value)

        #     count = len(live_angle_list)

        #     if count in [100, 500, 1000, 1500, 2000,5000,100000,150000]:

        #         calculate_width_cpk(live_width_list,name,5.27)
        #         calculate_angle_cpk(live_angle_list,name,1.10)        
        # if name == "neutral":
        
        #     angle_value = angle_terminal.get("raw_angle")
        #     width_value = widht_terminal.get("width_mm")

        #     neutral_angle_list.append(angle_value)
        #     neutral_width_list.append(width_value)

        #     count = len(neutral_angle_list)

        #     if count in [100, 500, 1000, 1500, 2000,5000,100000,150000]:

        #         calculate_width_cpk(neutral_width_list,name,5.28)
        #         calculate_angle_cpk(neutral_angle_list,name,0)        
    

    statuses = []
    for terminal in result:

        draw_image  = draw_img.draw_result(img,terminal)

        statuses.append(draw_image["status_width"])
        statuses.append(draw_image["status_angle"])
 
    if all(status == "OK" for status in statuses):

        cv.putText(img,"OK",( 30 , 80),cv.FONT_HERSHEY_SIMPLEX,2.5,(0,255,0),5,cv.LINE_8)

    else:
        cv.putText(img,"NG",( 30 , 80),cv.FONT_HERSHEY_SIMPLEX,2.5,(0,0,255),5,cv.LINE_8)    
   
    
    inspection_data = {
                    "module": module_name,
                    "status": "OK",
                    "result": result,
                    "draw_image": draw_image
                    }

    return inspection_data
            

def calculate_width_cpk(mm_list,name,size):
    NOMINAL = size
    TOL = 0.1
    LSL, USL = NOMINAL - TOL, NOMINAL + TOL

    data = np.array(mm_list)
    mean = np.mean(data)
    var  = np.var(data)
    std = np.std(data, ddof=1)
    cpk = min((USL-mean)/(3*std), (mean-LSL)/(3*std))
    
    print(f"========== {name} Width CPK Report ==========")
    print(f"Spec: {LSL:.2f} ~ {NOMINAL:.2f} ~ {USL:.2f} width")
    print(f"Count: {len(data)}")
    print(f"Mean: {mean:.4f} width")
    print(f"Std: {std:.4f} width")
    print(f"var: {var:.4f} width")
    print(f"Min   : {np.min(data):.4f}")
    print(f"Max   : {np.max(data):.4f}")
    print(f"Range : {np.max(data)-np.min(data):.4f}")
    print(f"CPK: {cpk:.2f}")

    print(f"Status: {'OK' if cpk >= 1.33 else 'NG'}")
    return cpk


def calculate_angle_cpk(angle_list,name,size):

    NOMINAL = size
    TOL = 0.6  # ±3 degree

    LSL = NOMINAL - TOL
    USL = NOMINAL + TOL

    data = np.array(angle_list)

    mean = np.mean(data)
    var = np.var(data)
    std = np.std(data, ddof=1)

    cpk = min(
        (USL - mean) / (3 * std),
        (mean - LSL) / (3 * std)
    )

    print(f"========== {name} Angle CPK Report ==========")
    print(f"Spec: {LSL:.2f} ~ {NOMINAL:.2f} ~ {USL:.2f} deg")
    print(f"Count: {len(data)}")
    print(f"Mean: {mean:.4f} deg")
    print(f"Std: {std:.4f} deg")
    print(f"var: {var:.4f} deg")
    print(f"Min   : {np.min(data):.4f}")
    print(f"Max   : {np.max(data):.4f}")
    print(f"Range : {np.max(data)-np.min(data):.4f}")
    print(f"CPK: {cpk:.2f}")

    print(f"Status: {'OK' if cpk >= 1.33 else 'NG'}")

    return cpk

# def calculate_Angle_repeatability(angle_list,name):

#     data = np.array(angle_list)

#     print(f"========== {name} Angle Repeatability ==========")
#     print(f"Count : {len(data)}")
#     print(f"Mean  : {np.mean(data):.4f}")
#     print(f"Std   : {np.std(data, ddof=1):.4f}")
#     print(f"Min   : {np.min(data):.4f}")
#     print(f"Max   : {np.max(data):.4f}")
#     print(f"Range : {np.max(data)-np.min(data):.4f}")

def img_healty(frame):
    """
    计算图像的均值和标准差（灰度图）
    """
    if frame is None:
        return None, None
    
    # 转为灰度图
    if len(frame.shape) == 3:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    else:
        gray = frame
    
    mean = np.mean(gray)   # ✅ 计算均值
    std = np.std(gray)     # ✅ 计算标准差
    
    return mean, std

def show_img_resut(frame_list):

    mean = np.array(frame_list[0])
    std = np.array(frame_list[1])
    

            
                    
    

                    








        
