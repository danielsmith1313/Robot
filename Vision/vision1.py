import time
import cv2
import numpy as np
from dual_g2_hpmd_rpi import motors, MAX_SPEED

x_last = 320
y_last = 180

#capturing video through webcam
cap=cv2.VideoCapture(0)               

while True:
        motors.enable()
        _, image = cap.read()   
        Whiteline = cv2.inRange(image, (195,195,195), (255,255,255))
        kernel = np.ones((3,3), np.uint8)
        Whiteline = cv2.erode(Whiteline, kernel, iterations=5)
        Whiteline = cv2.dilate(Whiteline, kernel, iterations=9) 
        img_blk,contours_blk, hierarchy_blk = cv2.findContours(Whiteline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        contours_blk_len = len(contours_blk)
        if contours_blk_len > 0 :
         if contours_blk_len == 1 :
          blackbox = cv2.minAreaRect(contours_blk[0])
          #whiteLineFound = True
         else:
           canditates=[]
           off_bottom = 0          
           for con_num in range(contours_blk_len):              
                blackbox = cv2.minAreaRect(contours_blk[con_num])
                (x_min, y_min), (w_min, h_min), ang = blackbox          
                box = cv2.boxPoints(blackbox)
                (x_box,y_box) = box[0]
                if y_box > 358 :                 
                 off_bottom += 1
                canditates.append((y_box,con_num,x_min,y_min))          
           canditates = sorted(canditates)
           if off_bottom > 1:       
                canditates_off_bottom=[]
                for con_num in range ((contours_blk_len - off_bottom), contours_blk_len):
                   (y_highest,con_highest,x_min, y_min) = canditates[con_num]           
                   total_distance = (abs(x_min - x_last)**2 + abs(y_min - y_last)**2)**0.5
                   canditates_off_bottom.append((total_distance,con_highest))
                canditates_off_bottom = sorted(canditates_off_bottom)         
                (total_distance,con_highest) = canditates_off_bottom[0]         
                blackbox = cv2.minAreaRect(contours_blk[con_highest])      
           else:                
                (y_highest,con_highest,x_min, y_min) = canditates[contours_blk_len-1]           
                blackbox = cv2.minAreaRect(contours_blk[con_highest])    
         (x_min, y_min), (w_min, h_min), ang = blackbox
         x_last = x_min
         y_last = y_min
         #if ang < -45 :
          #ang = 90 + ang
         if w_min < h_min and ang > 0:    
          ang = (90-ang)*-1
         if w_min > h_min and ang < 0:
          ang = 90 + ang          
         setpoint = 320
         error = int(x_min - setpoint) 
         ang = int(ang)  
         box = cv2.boxPoints(blackbox)
         box = np.int0(box)
         cv2.drawContours(image,[box],0,(0,0,255),3)     
         cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
         cv2.putText(image,str(error),(10, 320), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
         cv2.line(image, (int(x_min),200 ), (int(x_min),250 ), (255,0,0),3)

         if error < -10 and error > -150:
                 print("Go left")
                 if ang > -45:
                         motors.setSpeeds(120, 90)
                 if ang < -45:
                         motors.setSpeeds(250, 50)
         if error < -150:
                 print("Go left")
                 if ang > -45:
                         motors.setSpeeds(150, 90)
                 if ang < -45:
                         motors.setSpeeds(250, 50)
         if error > 10 and error < 150:
                 print("Go right")
                 if ang < 45:
                         motors.setSpeeds(90, 120)
                 if ang > 45:
                         motors.setSpeeds(50, 250)
         if error > 150 :
                 print("Go right")
                 if ang < 45:
                         motors.setSpeeds(90, 150)
                 if ang > 45:
                         motors.setSpeeds(50, 250)
         if error >= -10 and error <= 10:
                 print("Go straight")
                 if ang > -20 and ang < 20:
                         motors.setSpeeds(200, 200)
                 
                         
                         
                         
         
                
        cv2.imshow("orginal with line", image)  
        key = cv2.waitKey(1) & 0xFF     
        if key == ord("q"):
                cv2.destroyAllWindows()
                motors.disable()
                motors.setSpeeds(0, 0)
                break

