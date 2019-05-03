import numpy as np
import cv2 as cv

# BGR instead of RGB
# img[y,x]
img = cv.imread('img1.png')
opencv = img[115:144, 85:200]
img[3:32, 85:200] = opencv
cv.imshow('img', img)
cv.waitKey()
cv.destroyAllWindows()
# print(img[52,128])
# print(img.shape)
# print(img.size)
# print(img.dtype)