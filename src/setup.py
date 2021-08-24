import numpy as np
import cv2 as cv
import time 
import database as db

def nothing(x):
    pass

def trackbar(color):

    getMask = db.maskParam(color)
    color,lh, uh, ls, us, lv, uv,symbol = getMask[1],int(getMask[2]),int(getMask[3]),int(getMask[4]),int(getMask[5]),int(getMask[6]),int(getMask[7]),getMask[8]

    cv.namedWindow('image')
    # create trackbars for color change
    cv.createTrackbar('upper h','image',uh,360,nothing)
    cv.createTrackbar('lower h','image',lh,360,nothing)

    cv.createTrackbar('upper s','image',us,255,nothing)
    cv.createTrackbar('lower s','image',ls,255,nothing)

    cv.createTrackbar('upper v','image',uv,255,nothing)  
    cv.createTrackbar('lower v','image',lv,255,nothing)
    cv.createTrackbar(''+color+'','image',0,0,nothing)


    cap = cv.VideoCapture(0)
    while(cap.isOpened()):
      ret, frame = cap.read()
      
      if ret == True:
        frame,hsv = normalize(frame)
        img = frame.copy()
        img_mask = frame.copy()
        try:
            if cv.waitKey(33) == ord('s'):
                print("pressed s")
                db.updateParam(str(lh),str(uh),str(ls),str(us),str(lv),str(uv),color)
                print("saved")
                break

            # get current positions of four trackbars
            uh = cv.getTrackbarPos('upper h','image')
            lh = cv.getTrackbarPos('lower h','image')

            us = cv.getTrackbarPos('upper s','image')
            ls = cv.getTrackbarPos('lower s','image')

            uv = cv.getTrackbarPos('upper v','image')
            lv = cv.getTrackbarPos('lower v','image')

            lower = np.array([lh,ls,lv])
            upper = np.array([uh,us,uv])
            
            mask = cv.inRange(hsv, lower, upper)
            res = cv.bitwise_and(img_mask,img_mask, mask= mask)

            contours,_ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)

            if contours is not None :
                for contour in contours:
                    area = str(cv.contourArea(contour))

                    if area is not None:
                        if float(area) > 2000:
                            x,y,w,h = cv.boundingRect(contour)
                            puttext(res,area,(0,255,255),(30,30))
                            cv.rectangle(res,(x,y),(x+w,y+h),(0,255,255),3)

                bn,color_ = brightness(hsv)
                puttext(img,bn,color_,(10,30))
                puttext(img,'Press s for save',(255,0,0),(10,60))
                cv.imshow('image',mask)
                cv.imshow('img',img)
                cv.imshow('res',res)

        except Exception as e:
            print(e)

      else:
        break
    cap.release()
    cv.destroyAllWindows()    


def normalize(frame):
  kernel = np.ones((5,5),np.uint8)
  frame = cv.resize(frame,(500,400),interpolation=cv.INTER_LINEAR)
  hsv = frame.copy()

  hsv = cv.GaussianBlur(hsv,(13,13),0)
  hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
  hsv = cv.morphologyEx(hsv, cv.MORPH_OPEN, kernel)
  return frame,hsv

def brightness(hsv):
    h, s, v = cv.split(hsv)
    brightness = round(v.mean(),1)
    brightnessTxt = 'brightness:'+str(brightness)+' -> limit(140,200)'
    if 200 >= brightness >= 140:
        brightnessColor = tuple([0,255,0])
    else:
        brightnessColor = tuple([0,0,255])
    return brightnessTxt,brightnessColor

def puttext(frame,txt,color,location):
  font = cv.FONT_HERSHEY_SIMPLEX
  fontScale  = 0.7
  lineType = 2
  cv.putText(frame,txt, location, font,fontScale,color,lineType)

if __name__ == "__main__":
    print('lib import')
    # frame = cv.imread('datasets/21.jpg')
    # frame,hsv = normalize(frame)

    yellow =trackbar("'yellow'")
    green =trackbar("'green'")
    red =trackbar("'red'")
    white =trackbar("'white'")
    blue =trackbar("'blue'")
    black =trackbar("'black'")
