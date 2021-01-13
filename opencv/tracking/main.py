import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# Caminho do vídeo
cap = cv.VideoCapture("../video/jump.mp4")

term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

lower_white = np.array([0,0,165], dtype=np.uint8)
upper_white = np.array([180,255,255], dtype=np.uint8)


#lower_white = (0, 0, 100)
#upper_white = (169, 70, 255)
# Lower_white e upper white define qual distância de HSV deve ser filtrada.
# Os dois primeiros valores (0 -> 180, 0 -> 255) diz que deve pegar qualquer cor
# O último (165 -> 255) diz que deve pegar apenas as mais intensas (brilho alto).

# Fator de escala, 1 vai manter o vídeo nas dimensões originais, 0.5 diminuir pela metade, and so on.
scale_factor = 1
roi_size = 20 #px

def options(current_roi_n):
    print('\n'*8)
    print("Segure \'A\' para retroceder o vídeo.")
    print("Aperte \'S\' para esconder/mostrar as janelas.")
    print("Aperte \'R\' para esconder/mostrar as áreas de interesse.")
    print("Aperte \'H\' para calcular histograma da área de interesse seleciona(máscara \'white finder\' aplicada na área\
    de interesse)")
    print("Aperte \'B\' para projetar da área de interesse selecionada(máscara \'white finder\' aplicada na área de\
    interesse)")
    print("Aperte \'C\' para alternar entre as áreas de interesse.")
    print(f"\nÁrea de interesse atual: {current_roi_n}\n")


# Função que controla as ações quando o usuário dá um clique duplo
def select_roi(event, x, y, flags, param):
    global width, height, frame, roi_size, term_crit, white_filter, track_windows, current_roi

    if event == cv.EVENT_LBUTTONDBLCLK:

        size = int(roi_size/2)

        if x + roi_size >= width:
            x = width - roi_size
        elif x - size >= 0:
            x = x - size
        else:
            x = 0
        if y + roi_size >= height:
            y = height - roi_size
        elif y - size >= 0:
            y = y - size
        else:
            y = 0

        ret, track_window = cv.meanShift(white_filter, (x, y, roi_size, roi_size), term_crit)
        color = [0,255,0] if ret else [0,0,255]

        x, y, w, h = track_window
        i = len(track_windows)

        track_windows.append(track_window)
        frame = cv.rectangle(frame, (x, y), (x+w, y+h), color, 1, cv.LINE_8)

        (w2, h2), baseline = cv.getTextSize(str(i), cv.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        if (y - 3 - h2 - baseline) < 0:
            cv.putText(frame, str(i), (int((x + (w/2) - (w2/2))), int(y + roi_size + h2 + 3)), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv.LINE_AA)       
        else:
            cv.putText(frame, str(i), (int((x + (w/2) - (w2/2))), int(y - 3)), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv.LINE_AA)

        current_roi = i
        options(current_roi)
        cv.imshow("Tracking", frame)

# Essa função é usada pra resetar a função de clique do usuário quando o vídeo está sendo "reproduzido"
def reset(event, x, y, flags, param):
    pass

# Variáveis de controle
height, width = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
fps = cap.get(cv.CAP_PROP_FPS)
wait_time = 0
current_roi = -1
show_rois = True
show_windows = True
show_bp = False
show_options = False
track_windows = []
cv.namedWindow("Tracking")
cv.setMouseCallback("Tracking", select_roi)

options(0)

while True:
    sucess, original_frame = cap.read()

    if not sucess:
        break
    
    if show_options:
        options(current_roi)
        show_options = False

    current_frame = cap.get(cv.CAP_PROP_POS_FRAMES)

    if scale_factor != 1:
        original_frame = cv.resize(original_frame, (int(width * scale_factor), int(height * scale_factor)), interpolation=cv.INTER_LINEAR)

    frame = original_frame.copy()

    gray_frame = cv.cvtColor(original_frame, cv.COLOR_BGR2GRAY)
    ret, white_filter = cv.threshold(gray_frame, 165, 255, cv.THRESH_BINARY)    

    for i, track_window in enumerate(track_windows):        
        ret, track_window = cv.meanShift(white_filter, track_window, term_crit)

        track_windows[i] = track_window
        x, y, w, h = track_window

        color = [0,255,0] if ret else [0,0,255]

        (w2, h2), baseline = cv.getTextSize(str(i), cv.FONT_HERSHEY_SIMPLEX, 0.6, 1)

        if (y - 3 - h2 - baseline) < 0:
            cv.putText(frame, str(i), (int((x + (w/2) - (w2/2))), int(y + roi_size + h2 + 3)), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv.LINE_AA)       
        else:
            cv.putText(frame, str(i), (int((x + (w/2) - (w2/2))), int(y - 3)), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 1, cv.LINE_AA)

        frame = cv.rectangle(frame, (x, y), (x+w, y+h), color, 1, cv.LINE_8)
        cv.imshow("Tracking", frame)

        if show_rois:
            roi = frame[y:y+h, x:x+w]
            cv.imshow(f'Roi {i}', roi)
    
    cv.putText(frame, str(int(current_frame)), (2, 18), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    if show_bp or show_windows:
        hsv_frame = cv.cvtColor(original_frame, cv.COLOR_BGR2HSV)
        white_finder = cv.inRange(hsv_frame, lower_white, upper_white)

    if show_bp:
        x,y,w,h = track_windows[current_roi]

        roi = hsv_frame[y:y+h, x:x+w]
        roi_wf = white_finder[y:y+h, x:x+w]

        #roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

        roi_hist = cv.calcHist([roi], [0, 1], roi_wf, [180, 256], [0, 180, 0, 256])

        cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        dst = cv.calcBackProject([hsv_frame], [0, 1], roi_hist, [0,180,0,256],1)

        cv.imshow('Backprojection', dst)
        cv.imshow('HSV Roi', roi)
        cv.imshow('roi_wf', roi_wf)

    if show_windows:
        cv.imshow('White finder (HSV inRange)', white_finder)
        cv.imshow('White filter (Gray Scale threshold)', white_filter)
        cv.imshow('Gray frame', gray_frame)
        cv.imshow('HSV', hsv_frame)
    
    cv.imshow("Tracking", frame)
    
    key = cv.waitKey(wait_time)

    if key == ord('q') or key == ord('Q'):
        break

    elif (key == ord('c') or key == ord('c')):

        current_roi = current_roi + 1 if current_roi < len(track_windows) - 1 else 0
        options(current_roi)
        cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 1)

    elif (key == ord('b') or key == ord('B')):
        if len(track_windows) > 0:
            show_bp = True if show_bp == False else False
        
        if show_bp == False:
            cv.destroyWindow('HSV Roi')
            cv.destroyWindow('Backprojection')
            cv.destroyWindow('roi_wf')
        cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 1)

    elif key == ord('r') or key == ord('R'):

        show_rois = True if show_rois == False else False
        if show_rois == False:
            for x in range(len(track_windows)):
                cv.destroyWindow(f'Roi {x}')
        cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 1)

    elif key == ord('s') or key == ord('S'):

        show_windows = True if show_windows == False else False
        if show_windows == False:
            cv.destroyWindow('White finder (HSV inRange)')
            cv.destroyWindow('White filter (Gray Scale threshold)')
            cv.destroyWindow('Gray frame')
            cv.destroyWindow('HSV')
        cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 1)

    elif key == ord('p') or key == ord('P') or key == 13:
        
        if(wait_time == 0):
            wait_time = 15
            cv.setMouseCallback("Tracking", reset)
        else:
            wait_time = 0
            cv.setMouseCallback("Tracking", select_roi)

    elif wait_time == 0:

        if key == ord('a') or key == ord('A'):
            cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 2)

        elif (key == ord('h') or key == ord('H')):

            if len(track_windows) > 0:
                x,y,w,h = track_windows[current_roi]
                print('\n'*8)
                print('Aperte na janela do gráfico e em seguida \'Q\' (SEM CAPSLOCK) para sair.')
                print('\n'*3)
                show_options = True
                hsv_frame = cv.cvtColor(original_frame, cv.COLOR_BGR2HSV)
                white_finder = cv.inRange(hsv_frame, lower_white, upper_white)
                roi_hsv = hsv_frame[y:y+h, x:x+w]
                roi_wf = white_finder[y:y+h, x:x+w]
                # Como está calculando o histogram do canal 1 (0), ele vai de 0 até 180
                #roi_hist = cv.calcHist([roi_hsv], [0], None, [255], [0,256])
                roi_hist = cv.calcHist([roi_hsv], [2], roi_wf, [256], [0, 256])
                cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
                plt.plot(roi_hist) 

                plt.title('Histogram (value from HSV)')
                
                plt.xlabel('Bins')
                plt.ylabel('Intensity')

                plt.grid(True, alpha=.7, linestyle="--")

                plt.xlim([0,255])
                
                cv.imshow('Roi HSV', roi_hsv)
                cv.imshow('Roi WF', roi_wf)
                plt.show()
                cv.destroyWindow('Roi HSV')
                cv.destroyWindow('Roi WF')

            cap.set(cv.CAP_PROP_POS_FRAMES, current_frame - 1) 

cv.destroyAllWindows()

print("Programa finalizado!")