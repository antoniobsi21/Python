import numpy as np
import cv2 as cv

img1 = cv.imread('main.png')
img2 = cv.imread('logo.png')

rows1, cols1, channels1 = img1.shape
rows2, cols2, channels2 = img2.shape
roi = img1[rows1-rows2:rows1, 0:cols2]

img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 150, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

roi_bg = cv.bitwise_and(roi,roi,mask=mask)

img2_logo = cv.bitwise_and(img2, img2, mask=mask_inv)

dst = cv.add(roi_bg, img2_logo)
img1[rows1-rows2:rows1, 0:cols2] = dst

cv.imshow('img2', img2)
cv.imshow('img2gray', img2gray)
cv.imshow('maskimg2gray', mask)
cv.imshow('mask_inv', mask_inv)
cv.imshow('img1_bg', roi_bg)
cv.imshow('img2_fg', img2_logo)
cv.imshow('result', img1)

cv.waitKey(0)
cv.destroyAllWindows()
