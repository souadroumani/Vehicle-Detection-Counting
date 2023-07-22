import sys
import cv2
import numpy as np
#camera
cap = cv2.VideoCapture('videos/vehicle.mp4')

min_width_rect = 60 #min width rectangle
min_hieght_rect = 60 #min hieght rectangle 


count_line_postion = 580
count_line2_postion = 500


def center_handle(x,y,w,h):
    x1 = int(w/2)
    y1 = int(h/2)
    cx = x+x1
    cy = y+y1
    return cx , cy

#Initialize Substructor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

# algo = cv2.createBackgroundSubtractorMOG2()
#mixture of gaussians 


detect = []
offset = 6 # allowanle error between pixel
offset1 = 4
coming_counter = 0 
going_counter = 0 




while True :
    ret,frame1=cap.read()
    gray = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)   
    blur =cv2.GaussianBlur(gray,(3,3),5)
    
    #applying on each frame
    img_sub = algo.apply(blur)
    
    dilat = cv2.dilate(img_sub,np.ones((5,5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    dilatada = cv2.morphologyEx(dilat , cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada , cv2.MORPH_CLOSE, kernel)
    
    counterShape , h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #here we add the line and set the color and 
    
    cv2.line(frame1,(30,count_line_postion),(550, count_line_postion),(255,127,0),7)
    cv2.line(frame1,(710,count_line2_postion),(1080, count_line2_postion),(127,255,0),7)
    
    
    
    for (i,c) in enumerate(counterShape):
        (x,y,w,h) = cv2.boundingRect(c)
        validate_counter = (w >= min_width_rect) and (h >= min_hieght_rect)
        if not validate_counter:
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2) 
        
        
        if x < 680 :
            cv2.putText(frame1,"ComVe:" + str(coming_counter),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(255,244,0),2)
        else:
            cv2.putText(frame1,"GoVe:" + str(going_counter),(x,y-20),cv2.FONT_HERSHEY_TRIPLEX,1,(244,255,0),2)        
            
        center = center_handle(x,y,w,h)
        detect.append(center)
        cv2.circle(frame1,center,4,(0,0,255),-1)
        
        for(x,y) in detect:
            if y < (count_line_postion + offset) and y > (count_line_postion  - offset) and x < 680 :
                coming_counter +=1 
                cv2.line(frame1,(30,count_line_postion),(550, count_line_postion),(0,127,255),7)       
                detect.remove((x,y))
                print("Coming Vehicle Counter" + str(coming_counter))
            
            elif y < (count_line2_postion + offset1) and y > (count_line2_postion  - offset1) and x > 680 :
                going_counter +=1 
                cv2.line(frame1,(710,count_line2_postion),(1080, count_line2_postion),(100,100,255),)      
                detect.remove((x,y))
                print("Going Vehicle Counter" + str(going_counter))    
            
            
            
    cv2.putText(frame1,"Coming vehicles counter: " + str(coming_counter),(50,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,200),3)        
    cv2.putText(frame1,"Going vehicles counter: " + str(going_counter),(800,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,200,200),3)        
        
        
        
        
        

    # cv2.imshow("Detecter" , dilatada)
    # for here he using filter and apply it on video become the vehicle in white and bachground in black 
    
    
    
    
    
    
    
    
    cv2.imshow("video Original" , frame1)
    
    if cv2.waitKey(1) == 13:
        break
    
    
cv2.destroyAllWindows()
cap.release()    
