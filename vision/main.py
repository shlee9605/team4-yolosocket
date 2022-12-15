import cv2
import torch
import numpy as np
from socket import *
from select import *
from time import sleep

HOST = '192.168.0.120'  # Edukit Port
PORT = 2004
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket() # Open Socket
# clientSocket.connect(ADDR)
# print('Connection PLC Success!')

model_label = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/dices5/weights/last.pt', source='local') # Read Train Model
webcam = cv2.VideoCapture(0)

readings = [-1, -1]
display = [0, 0]

Circle_Inertia = 0.6
Gaussian_ksize = (7, 7)
canny_threshold_min = 150
canny_threshold_max = 250

params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = True
params.minInertiaRatio = Circle_Inertia

detector = cv2.SimpleBlobDetector_create(params)    #Blob 검출

if not webcam.isOpened():   # Catch Error
    print("Could not open webcam")
    exit()

while webcam.isOpened():    # If Not
    status, frame = webcam.read()   # Read Cam

    if status:

        dst = frame.copy()  # For dot detect

        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model_label(imgRGB)
        results = results.pandas().xyxy[0][['name','xmin','ymin','xmax','ymax']]

        dice = [0, 0, 0, 0]
        cup = [0, 0, 0, 0]

        for num, i in enumerate(results.values):
            if i[0] == 'Dice' and dice[0] == 0 :                
                dice = [int(i[1]), int(i[2]), int(i[3]), int(i[4])]
            if i[0] == 'Cup' and cup[0] == 0 :
                cup = [int(i[1]), int(i[2]), int(i[3]), int(i[4])]
            if dice[0] != 0 and cup[0] != 0:
                break


        fair = "false"
        if dice[0] > cup[0] and dice[1] > cup[1] and dice[2] < cup[2] and dice[3] < cup[3]:
            fair = "true"

        if fair == "true" :
            cv2.putText(imgRGB, 'Dice', (dice[0], dice[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 2)
            cv2.rectangle(imgRGB, (dice[0], dice[1]), (dice[2], dice[3]), (0, 0, 255), 3)
            cv2.putText(imgRGB, 'Cup', (cup[0], cup[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 2)
            cv2.rectangle(imgRGB, (cup[0], cup[1]), (cup[2], cup[3]), (0, 0, 255), 3)
        else : 
            cv2.putText(imgRGB, 'Dice', (dice[0], dice[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 2)
            cv2.rectangle(imgRGB, (dice[0], dice[1]), (dice[2], dice[3]), (255, 0, 0), 3)
            cv2.putText(imgRGB, 'Cup', (cup[0], cup[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 2)
            cv2.rectangle(imgRGB, (cup[0], cup[1]), (cup[2], cup[3]), (255, 0, 0), 3)


        frame_blurred = cv2.GaussianBlur(dst, Gaussian_ksize, 1)      #가우시안
        frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)    #흑백
        frame_canny = cv2.Canny(frame_gray, canny_threshold_min, canny_threshold_max, apertureSize=3, L2gradient=True)  #캐니 임계

        keypoints = detector.detect(frame_canny)    #검출기

        num = len(keypoints)    #검출 숫자
        readings.append(num)

        im_with_keypoints = cv2.drawKeypoints(imgRGB, keypoints, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  #검출
        cv2.putText(im_with_keypoints, "dice : " + str(num) + ", fair : " + fair, (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        imgBGR = cv2.cvtColor(im_with_keypoints, cv2.COLOR_RGB2BGR)
        cv2.imshow("test2", imgBGR)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if fair == "true" :
            if readings[-1] == readings[-2] == readings[-3] == readings[-4] == readings[-5] == readings[-6]:    #10회 반복해서 같으면 송신
                socketTxData = bytes([76,83,73,83,45,88,71,84,0,0,0,0,160,51,0,0,22,0,0,0,88,0,2,0,0,0,1,0,8,0,37,68,87,48,49,49,48,48,2,0,])                                        
                num_little = num.to_bytes(2, 'little')

                if num != 0:
                    print("num is " + str(num))
                    print("value is " + fair)
                    try:
                        clientSocket = socket(AF_INET, SOCK_STREAM)
                        clientSocket.connect(ADDR)
                        print('Connection PLC Success!')
                        clientSocket.send(socketTxData + num_little)
                        # msg = clientSocket.recv(1024)
                    except  Exception as e:
                        print(e)
                clientSocket.close()
                print('close PLC Success!')
                readings.append(0)
                sleep(1)    # PLC는 빠르게 데이터를 받지 못하므로 반드시 sleep 1처리

webcam.release()
cv2.destroyAllWindows()


