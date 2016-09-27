#!/usr/bin/python

#### this program read two image and blend it by using Image Pyramid

import cv2
import numpy as np,sys

A = cv2.imread('apple.jpeg')
B = cv2.imread('orange.jpeg')
rows,cols = A.shape[:2]
B = cv2.resize(B,(cols,rows),interpolation = cv2.INTER_CUBIC)
print A.shape[:2]
print B.shape[:2]
### generate Gaussian Pyramid
G = A.copy()
gpA = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    #print G.shape[:2]
    gpA.append(G)

G = B.copy()
gpB = [G]
for i in range(6):
    G = cv2.pyrDown(G)
    gpB.append(G)
### generate lapacian Pyramid
lpA = [gpA[5]]
for i in range(5,0,-1):
    size = (gpA[i-1].shape[1], gpA[i-1].shape[0])	
    #size = (gpA[i-1]).shape[:2]
    #print size
    GE = cv2.pyrUp(gpA[i],dstsize = size)
    #rows,cols = (gpA[i-1]).shape[:2]
    #print rows,cols
    #print '#############'
    #rows,cols = GE.shape[:2]
    #print rows,cols
    L = cv2.subtract(gpA[i-1],GE)
    lpA.append(L)


lpB = [gpB[5]]
for i in range(5,0,-1):
    size = (gpB[i-1].shape[1], gpB[i-1].shape[0])
    #size = (gpB[i-1]).shape[:2]
    GE = cv2.pyrUp(gpB[i],dstsize = size)
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)


#### Add the two Image
LS = []
for la,lb in zip(lpA,lpB):
    
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols/2] , lb[:,cols/2:]))
    LS.append(ls)


#### reconstruct the image
ls_ = LS[0]
for i in range(1,6):
    size = (LS[i].shape[1], LS[i].shape[0])
    ls_ = cv2.pyrUp(ls_,dstsize = size)
    ls_ = cv2.add(ls_,LS[i])
    


real  =np.hstack((A[:,:cols/2],B[:,cols/2:]))


cv2.imwrite('Pyramid_image.jpg',ls_)
cv2.imwrite('Direct_blend.jpg',real)

    


