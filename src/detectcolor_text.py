import numpy as np
import cv2 as cv
import setup as set
import database as db

def maskParam(model): # get parameter models from database
    paramColor = []
    raw = list(db.model("'"+model+"'"))
    masterColor = raw[2:]
    model = raw[1]
    for color in masterColor:
        getMask = db.maskParam("'"+color+"'")   
        paramColor.append(getMask)
    return paramColor,model,masterColor

def detectColor(frame,hsv,paramColor,masterColor):
  try:
    img = frame.copy()

    x0 = 0  
    n=0

    result = 'OK'
    resultColor = tuple([0,255,0])

    location = {}
    sort = []

    for getMask in paramColor:
        color,lh, uh, ls, us, lv, uv,symbol = getMask[1],int(getMask[2]),int(getMask[3]),int(getMask[4]),int(getMask[5]),int(getMask[6]),int(getMask[7]),getMask[8]
        
        lower = np.array([lh,ls,lv])
        upper = np.array([uh,us,uv])    
        mask = cv.inRange(hsv, lower, upper)
        contours,_ = cv.findContours(mask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        
        if contours is not None :
          for contour in contours:
            area = str(cv.contourArea(contour))
            if area is not None:
              if float(area) > 5000:
                x,y,w,h = cv.boundingRect(contour)

                if x>x0:
                    rectanColors = tuple([0,128,0])
                    if result == 'OK':
                      resultColor = tuple([0,255,0])
                else:
                    rectanColors = tuple([0,0,255])
                    result = 'NG'
                    resultColor = tuple([0,0,255])
                    
 
                set.puttext(img,symbol,(220,220,220),(x+1,y+100)) # text rectangle
                cv.rectangle(img,(x,y),(x+w,y+h),rectanColors,1) # rectangle
                x0 = x
         
                location[''+color+'']= x
    
 
    if len(location) > 1:            
      sort_orders = sorted(location.items(), key=lambda x: x[1], reverse=False)
      for i in sort_orders:
        sort.append(i[0])
    
    c = 30 
    e = 30 
    for j in range(len(masterColor)):
      set.puttext(img,'MASTER',(255,0,0),(10,120))
      set.puttext(img,str(masterColor[j]),(255,0,0),(10,120+c))
      c = c+30 

    if sort is not None:
      for k in range(len(sort)): 
        set.puttext(img,'RESULT',(0,128,0),(100,120))
        resultColor = tuple([0,128,0])
        if str(sort[k]) != str(masterColor[k]):
          resultColor = tuple([0,0,255])
        set.puttext(img,str(sort[k]),resultColor,(100,120+e))
        e = e+30


    # check detect all color
    n = len(location)
    if n != len(paramColor):
        result = 'NG'
        resultColor = tuple([0,0,255])
    set.puttext(img,'cont color:'+str(n),(220,220,220),(10,90)) 

    set.puttext(img,'model:'+model,(220,220,220),(10,60))
    set.puttext(img,result,resultColor,(450,30))               
    bn,color_ = set.brightness(hsv)
    set.puttext(img,bn,color_,(10,30))
    #imgshow
    return img

  except Exception as e:
    print(e)

if __name__ == "__main__":
    print('lib import')

    paramColor,model,masterColor = maskParam('A001')

    cap = cv.VideoCapture(0)
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
          try:
              frame,hsv = set.normalize(frame)
              result = detectColor(frame,hsv,paramColor,masterColor)
              cv.namedWindow('image',flags=cv.WINDOW_NORMAL)
              cv.resizeWindow('image',1280,800)
              cv.imshow('image', result)
          except Exception as e:
            print(e)
          if cv.waitKey(1) & 0xFF == ord(' '):
            break
      else:
        break
    cap.release()
    cv.destroyAllWindows()    
