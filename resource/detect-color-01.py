import cv2 as cv
import numpy as np

area = 500
result = 'init'
result_color = (0,0,0)
x_r = 0
x_y = 0 

lower_y = np.array([15,120,20])
upper_y = np.array([35,255,255])

lower_r = np.array([0,120,20])
upper_r = np.array([10,255,255])

lower_g = np.array([50,20,20])
upper_g = np.array([70,255,255])

video = cv.VideoCapture(0)

while True:
    success,img = video.read()
    image = cv.cvtColor(img,cv.COLOR_BGR2HSV)

    mask_y = cv.inRange(image,lower_y,upper_y)
    mask_r = cv.inRange(image,lower_r,upper_r)
    mask_g = cv.inRange(image,lower_g,upper_g)

    contours_y,_ = cv.findContours(mask_y,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours_r,_ = cv.findContours(mask_r,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    contours_g,_ = cv.findContours(mask_g,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

    if len(contours_y) != 0 :
       for contour_y in contours_y:
           if cv.contourArea(contour_y) > area:
               x_y,y_y,w_y,h_y = cv.boundingRect(contour_y)
               cv.putText(img,'Y',(x_y,x_y),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
               cv.rectangle(img,(x_y,x_y),(x_y+w_y,y_y+h_y),(0,255,255),3)
               #print('yellow',x_y,y_y)

    if len(contours_r) != 0 :
       for contour_r in contours_r:
           if cv.contourArea(contour_r) > area:
               x_r,y_r,w_r,h_r = cv.boundingRect(contour_r)
               cv.putText(img,'R',(x_r,y_r),cv.FONT_HERSHEY_SIMPLEX,1,(0,0,255),3)
               cv.rectangle(img,(x_r,y_r),(x_r+w_r,y_r+h_r),(0,0,255),3)
               #print('red',x_r,y_r)
    
    if len(contours_g) != 0 :
       for contour_g in contours_g:
           if cv.contourArea(contour_g) > area:
               x_g,y_g,w_g,h_g = cv.boundingRect(contour_g)
               cv.putText(img,'G',(x_g,y_g),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
               cv.rectangle(img,(x_g,y_g),(x_g+w_g,y_g+h_g),(0,255,0),3)

    if len(contours_r) and len(contours_y) != 0:
        if cv.contourArea(contour_r) and cv.contourArea(contour_y) > 150:
            print('r',x_r)
            print('y',x_y)
            if int(x_r) > int(x_y):  
                result = 'OK'
                result_color = (0,255,0)
            else:
                result = 'NG'
                result_color = (0,0,255)

    cv.putText(img,result,(30,100),cv.FONT_HERSHEY_SIMPLEX,3,result_color,3)

    cv.imshow('Mask_r',mask_r)
    cv.imshow('Mask_y',mask_y)
    cv.imshow('Mask_g',mask_g)
    cv.imshow('webcam',img)
    
    cv.waitKey(1)
cv.destroyAllWindows()