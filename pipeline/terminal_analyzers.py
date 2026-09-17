from pipeline.base_inspection import TerminalInspection
import cv2 as cv
import numpy as np

class TerminalAnalyzer(TerminalInspection):
    
    def __init__(self):
        
  
        self.kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,7))
        self.big_kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,9))
        self.kernel_small = cv.getStructuringElement(cv.MORPH_RECT,(3,5))
        self.kernel_medium = cv.getStructuringElement(cv.MORPH_ELLIPSE , (3,5))
        self.blur_size = (19, 21)
        super().__init__()

    def choose_best_channel(self, image, choose_min = False):
    
            module = "choose_best_channel"
    
            if image is None:
                return {"module": module, "message": "Image is None", "status": "ERROR"}
    
            if len(image.shape) != 3:
                return {"module": module, "message": "Image wrong format", "status": "ERROR"}
    
            _, std = cv.meanStdDev(image)
    
            std_b, std_g, std_r = std.ravel()
            std_values = [std_b, std_g, std_r]
    
            best_idx = np.argmin(std_values) if choose_min else np.argmax(std_values)
    
            return {
                "module": module,
                "message": "Choose channel successfully",
                "status": "OK",
                "best_idx": best_idx,
                "best_name": ["B", "G", "R"][best_idx],
                "best_value": std_values[best_idx],
                "std_b": std_b,
                "std_g": std_g,
                "std_r": std_r,
            }
        
   
    def preprocess_bv(self, frame):

        module_name = "preprocess_bv"

        if frame is None:
            return {"module": module_name,"status": "ERROR","msg": "Image is None","img": None}

        # best_id = self.choose_best_channel(frame)[0]

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        bgr_r = frame[:, :, 2]
        v = hsv[:, :, 2]

        # best_img = self.choose_best_channel(frame)
        # best_idx = best_img.get("best_idx")

        # bgr_r = frame[:, :, best_idx]


        # # # 用CLAHE先提对比度，再融合
        # clahe = cv.createCLAHE(clipLimit=1.5, tileGridSize=(12,12))
        # b_eq = clahe.apply(bgr_r)
        # v_eq = clahe.apply(v)
    
        # fusion = cv.addWeighted(bgr_r, 0.7, v, 0.3, 0)# B+V 融合

        blur = cv.GaussianBlur(bgr_r,self.blur_size,0)
      

        if self.debug["image_health"]:
         # debug image health 
            img_health = np.zeros_like(frame)
            b_mean = np.mean(bgr_r)
            blur_mean = np.mean(blur)# 平均亮度
            fusion_std  = np.std(blur) # 对比度
            v_mean = np.mean(v)# 整体亮度
            lap = cv.Laplacian(bgr_r, cv.CV_64F).var() # 清晰度
            color = (255, 255, 255) 
            cv.putText(img_health,f"Blur Brightness : {blur_mean:.2f}",(30,30),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"B Mean           : {b_mean:.2f}",(30,90),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"Contrast        : {fusion_std:.2f}",(30,120),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"V Mean          : {v_mean:.2f}",(30,150),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"Sharpness       : {lap:.2f}",(30,180),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.imshow("img_health",img_health)
    
        return{
                    "module": module_name,
                    "status": "OK",
                    "msg"   : " B + V preprocessing completed",
                    "img":blur
                } 

    def preprocess_gray_v(self,frame):
    
        module_name = "preprocess_gray_v"

        if frame is None:
            return {
                "module": module_name,
                "status": "ERROR",
                "msg": "Image is None",
                "img": None
            }

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
    
        fusion = cv.addWeighted(gray, 0.7, v, 0.3, 0)# B+V 融合
        
        blur = cv.GaussianBlur(fusion,self.blur_size,0)# 去除小杂讯 

        blur = np.where(blur < 110,blur,255)

        if self.debug["image_health"]:
            # debug image health 
            img_health = np.zeros_like(frame)
            fusion_mean = np.mean(blur)# 平均亮度
            fusion_std  = np.std(blur) # 对比度
            v_mean = np.mean(v)# 整体亮度
            lap = cv.Laplacian(gray, cv.CV_64F).var() # 清晰度
            color = (255, 255, 255) 
            cv.putText(img_health,f"Mean Brightness : {fusion_mean:.2f}",(30,30),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"Contrast        : {fusion_std:.2f}",(30,60),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"V Mean          : {v_mean:.2f}",(30,90),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.putText(img_health,f"Sharpness       : {lap:.2f}",(30,120),cv.FONT_HERSHEY_SIMPLEX,0.5,color,1,cv.LINE_8)
            cv.imshow("img_health",img_health) 

        return{
                    "module": module_name,
                    "status": "OK",
                    "msg"   : "Gray + V preprocessing completed",
                    "img":blur
                } 

    def binary_terminal_contours(self,img,name):

        module_name = "binary_terminal_contours"

        if img is None:
            return {
                "module": module_name,
                "status": "ERROR",
                "msg": "Image is None",
                "img": None
            }

        if name == "ground":
        # 方案1：手动阈值（根据实验确定）
            # otsu,binary = cv.threshold(img,0,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
             # Sobel 梯度（直接找边缘）
            scharrx = cv.Scharr(img, cv.CV_64F, 1, 0)
            scharry = cv.Scharr(img, cv.CV_64F, 0, 1)
            mag = np.sqrt(scharrx**2 + scharry**2)
            mag = np.uint8(np.clip(mag / np.max(mag) * 255, 0, 255))
            
            # 用梯度幅值代替二值图
            # finish_binary = mag  # 不是真正的二值图，而是梯度图
            
     
            threshold = np.mean(mag) + 0.5 * np.std(mag)
            _, binary = cv.threshold(mag, threshold, 255, cv.THRESH_BINARY)
            # cv.imshow("ground",binary)

        else:    
        
            otsu,binary = cv.threshold(img,0,255,cv.THRESH_BINARY_INV|cv.THRESH_OTSU)
    

        # binary = cv.adaptiveThreshold(img,150, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 99, 5)

        match name:

            case "ground":
                dilate = cv.dilate(binary, self.kernel_small, iterations=1)
                erode = cv.erode(dilate, self.kernel, iterations=1)
                # cv.imshow("ground",erode)

            case "live":
                
                dilate = cv.dilate(binary, self.kernel_medium, iterations=3)
                erode = cv.erode(dilate, self.kernel, iterations=1)
      
                # erode = cv.morphologyEx(binary, cv.MORPH_OPEN, self.kernel)

            case "neutral":
                dilate = cv.dilate(binary, self.kernel_medium, iterations=3)
                erode = cv.erode(dilate, self.kernel, iterations=1) 
              

            case _:
  
                pass         

        finish_bianry = cv.medianBlur(erode,3)

        contour = cv.findContours(finish_bianry,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]

        valid_contour = [cnt for cnt in contour if cv.contourArea (cnt) > 2000]   # 过滤小杂点

        if not valid_contour:
            # 找不到轮廓就返回 ERROR，
            return {"module": module_name,"status": "ERROR","msg": "No terminal contour found!","img": finish_bianry}

        largest = max(valid_contour, key=cv.contourArea)# 最大轮廓

        x,y,w,h = cv.boundingRect(largest)  # 计算外接矩形

        if self.debug["contour"]:
            draw_img = img.copy()
            cv.drawContours(draw_img,valid_contour,-1,(0,255,0),1)
            cv.imshow(name,draw_img)
            cv.waitKey(0)

        if self.debug["binary"]:
            cv.imshow(name,finish_bianry)
            cv.waitKey(0)
            cv.destroyAllWindows()


        return{
            "module": module_name,
            "status": "OK",
            "contour_len":len(valid_contour),
            "draw_contours":valid_contour,
            "max_area": largest,
            "bounding_x": x,
            "bounding_y": y,
            "bounding_w": w,
            "bounding_h": h,
            "img":finish_bianry
        }