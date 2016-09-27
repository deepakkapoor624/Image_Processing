import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    ### take each frame
    _, frame = cap.read()
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    ### define range of blue color in HSV
    red = np.uint8([[[0,255,0]]])
    hsv_red = cv2.cvtColor(red,cv2.COLOR_BGR2HSV)
    #print hsv_red
    lower_red = np.array([0,50,50])
    upper_red = np.array([20,255,255])

    ###  THreshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv , lower_red,upper_red)
    
    #### bitwise AND mask and original image
    res = cv2.bitwise_and(frame,frame , mask = mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF     
    if k==27:
        break

cv2.destroyAllWindows()
