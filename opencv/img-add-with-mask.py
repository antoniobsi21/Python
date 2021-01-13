import numpy as np
import cv2 as cv
from sys import exit
from os import listdir

img1 = cv.imread('imgs/fundo.png')
# img1 deve ser maior que img2
img2 = cv.imread('imgs/logo.png')
img2 = cv.resize(img2[0:175, :], None, fx=0.6, fy=0.6, interpolation = cv.INTER_CUBIC)

rows1, cols1, channels1 = img1.shape
rows2, cols2, channels2 = img2.shape
contC = 0
inc = 5
going = True

img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
ret, mask = cv.threshold(img2gray, 20, 255, cv.THRESH_BINARY)
mask_inv = cv.bitwise_not(mask)

img2_logo = cv.bitwise_and(img2, img2, mask=mask)

while 1:
	result = img1.copy()
	if cols2 + contC > cols1:
		going = False
		contC = cols1 - cols2
	elif contC < 0:
		going = True
		contC = 0
	roi = img1[rows1-rows2:rows1, contC:cols2+contC]

	roi_bg = cv.bitwise_and(roi,roi,mask=mask_inv)

	dst = cv.add(roi_bg, img2_logo)
	result[rows1-rows2:rows1, contC:cols2+contC] = dst

	cv.imshow('result', result)
	key = cv.waitKey(1)
	if key == ord('q'):
		break
	elif key == ord('p'):
		key2 = cv.waitKey(0)
		if key2 == ord('q'):
			exit()
	if going:
		contC += inc
	else:
		contC -= inc

cv.destroyAllWindows()