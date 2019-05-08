#XY Integrado com vídeo

import cv2
import numpy as np
import imutils
from matplotlib import pyplot as plt
inputMode = False
mouse = False
ix,iy = -1,-1
# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy
    if inputMode and event == cv2.EVENT_LBUTTONDBLCLK:
        #print("teste")
        #print (x,y)
        #cv2.circle(frame,(x,y),10,(255,0,0),2)
        cv2.imshow("Frame", frame)
        ix,iy = x,y
        

# Create a black image, a window and bind the function to window
cv2.namedWindow('Frame')
cv2.setMouseCallback('Frame',draw_circle)

cap = cv2.VideoCapture('teste_Trim.mp4')
# Setup the termination criteria, either 10 iteration or move by atleast 1 pt
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

while True:
	inputMode = False #isso faz com que se capture o duplo click do mouse
	#apenas quando a tecla p for pressionada
	
	ret, frame = cap.read()
	if ret == True:
	#esse if e o else break abaixo garantem que o video acabe corretamente,
	#caso contrario, será dado a seguinte mensagem no final do video
	#cv2.error: OpenCV(4.1.0) (-215:Assertion failed) size.width>0 && size.height>0 in function 'cv::imshow'
		
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(30) & 0xFF

		if key==ord("p"): #pausa o video e aguarda o usuário dar duplo click
			inputMode = True
			key = cv2.waitKey(0) & 0xFF #waitKey(0) faz a imagem ficar parada
			r,h,c,w = iy-30,70,ix-30,70  # simply hardcoded the values  y, largura retangulo, x, altura retangulo - Joelmir
			track_window = (c,r,w,h)
			# set up the ROI for tracking
			roi = frame[r:r+h, c:c+w]
			hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(hsv_roi, np.array((17., 0.,0.)), np.array((180.,255.,255.))) #Achei esses valores com ajuda do HSV_Real_Time
			cv2.imshow("teste", mask)
			roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])#Isso calcula o histograma da mascara
			#Mostra o histograma calculado
			plt.plot(roi_hist)
			plt.show()
			cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
			mouse = True

		

		elif key==ord("q"): #saia do video
			break		
		
		elif mouse == True: 
			#print("Vitoria")
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#cv2.imshow('teste3',hsv)
			dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)
			#plt.plot(dst)
			#plt.show()

			# apply meanshift to get the new location
			ret, track_window = cv2.meanShift(dst, track_window, term_crit)
			# Draw it on image
			x,y,w,h = track_window
			cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0),2) #Cor Azul
			cv2.imshow('Aplicando Meanshift',frame)
			#nao estava pegando o Lower e Upper pq o quadrado estava em BGR ao invés de HSV		
			# Load an color image
			hsv2 = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #HSV de todo ambiente, inclusive o quadrado azul
	        #peguei o Lower e Upper com o click_and_crop
			Lower = (120, 255, 86)
			Upper = (120, 255, 255)
			# Threshold the HSV image to get only white colors
			threshold = cv2.inRange(hsv2, Lower, Upper)
			#cv2.imshow('threshold',threshold)
			# find contours in the thresholded image
			cnts = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			
			# loop over the contours
			for c in cnts:
			# compute the center of the contour
				M = cv2.moments(c)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				print("X = ", cX, "Y = ",cY)
				# draw the contour and center of the shape on the image
				#cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
				cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1) #7 é o tamanho do circulo
				#cv2.putText(frame, "center", (cX - 20, cY - 20),
				#cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
 
				# show the image
				cv2.imshow("Image", frame)
				#cv2.waitKey(0)

		
	else:
		break		
cv2.destroyAllWindows()
