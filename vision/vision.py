import cv2
import numpy as np
from socket import *
from select import *
import sys
from time import sleep

HOST = '192.168.0.120'
PORT = 2004
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(ADDR)

print('Connection PLC Success!')

cap = cv2.VideoCapture(0) # 0 or 1

readings = [-1, -1]
display = [0, 0]

Circle_Inertia = 0.6
Gaussian_ksize = (7, 7)
canny_threshold_min = 100
canny_threshold_max = 250

params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = True
params.minInertiaRatio = Circle_Inertia

detector = cv2.SimpleBlobDetector_create(params)    #Blob 검출

while True:
    ret, frame = cap.read()
    
    frame_blurred = cv2.GaussianBlur(frame, Gaussian_ksize, 1)      #가우시안
    frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)    #흑백
    frame_canny = cv2.Canny(frame_gray, canny_threshold_min, canny_threshold_max, apertureSize=3, L2gradient=True)  #캐니 임계
    
    keypoints = detector.detect(frame_canny)    #검출기

    num = len(keypoints)    #검출 숫자
    readings.append(num)

    im_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  #검출
    cv2.putText(im_with_keypoints, str(num), (500, 250), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 5, (0, 255, 0))

    cv2.imshow("test", im_with_keypoints)   #출력
    if cv2.waitKey(1) & 0xFF == ord('q'):  #종료(q)
        break

    if readings[-1] == readings[-2] == readings[-3] == readings[-4] == readings[-5] == readings[-6]:    #6회 반복해서 같으면 송신
        socketTxData = bytes([76,83,73,83,45,88,71,84,0,0,0,0,160,51,0,0,22,0,0,0,88,0,2,0,0,0,1,0,8,0,37,68,87,48,49,49,48,48,2,0,])                                        
        num_little = num.to_bytes(2, 'little')

        if num != 0:
            print("num is " + str(num))
            try:
                clientSocket.send(socketTxData + num_little)
                msg = clientSocket.recv(1024)
                print(msg)
            except  Exception as e:
                print(e)

frame.release()
cv2.destroyAllWindows()

