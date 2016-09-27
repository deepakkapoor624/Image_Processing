import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test.jpeg',0)
edges = cv2.Canny(img,80,200)

plt.subplot(121), plt.imshow(img,'gray'),plt.title('Original Image')
plt.subplot(122), plt.imshow(edges,'gray'),plt.title('Canny Image')

plt.show()
