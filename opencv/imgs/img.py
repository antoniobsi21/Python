import numpy as np
import cv2 as cv

car = cv.imread('car.jpg')
road = cv.imread('road.jpg')

car2gray = cv.cvtColor(car, cv.COLOR_BGR2GRAY)

dst = cv.addWeighted(car,0.5, road,1, 0)

ret, threshold = cv.threshold(car2gray, 5, 255, cv.THRESH_BINARY)

cv.imshow('threshold', threshold)
cv.imshow('car2gray',car2gray)
cv.imshow('car', car)
cv.imshow('road', road)
cv.imshow('dst', dst)

cv.waitKey()
cv.destroyAllWindows()