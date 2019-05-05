import numpy as np
import cv2 as cv
import sys

cap = cv.VideoCapture('videos/teste.mp4')

font = cv.FONT_HERSHEY_SIMPLEX
color = (255, 255, 255)
while cap.isOpened():
	ret, frame = cap.read()

	if not ret:
		print("Can't receive frame (stream end?). Exiting ...")
		break

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	
	frameAtual = cap.get(1)
	cv.putText(gray, str(frameAtual), (0,17), font, 0.5, color, 2, cv.LINE_AA)

	cv.imshow('frame', gray)

	key = cv.waitKey(25)
	if key == ord('q'):
		break
	elif key == ord('p'):
		while 1:
			ret, frame = cap.read()

			gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

			cv.putText(gray, str(frameAtual), (0,17), font, 0.5, color, 2, cv.LINE_AA)

			cv.imshow('frame', gray)
			key2 = cv.waitKey(0)
			if key2 == ord('p'):
				break
			elif key2 == ord('q'):
				sys.exit()
			elif key2 == ord('k'):
				cap.set(1, frameAtual-1)
				frameAtual = cap.get(1)
				cv.putText(gray, str(frameAtual), (0,17), font, 0.5, color, 2, cv.LINE_AA)
			else:
				cap.set(1, frameAtual+1)
				frameAtual = cap.get(1)
				cv.putText(gray, str(frameAtual), (0,17), font, 0.5, color, 2, cv.LINE_AA)

cap.release()
cv.destroyAllWindows()