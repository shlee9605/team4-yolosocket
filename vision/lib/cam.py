import cv2
from socket import *
from time import sleep

HOST = '192.168.0.120'  # Edukit Port
PORT = 2004
ADDR = (HOST,PORT)

readings = [-1, -1]

Circle_Inertia = 0.6
Gaussian_ksize = (7, 7)
canny_threshold_min = 150
canny_threshold_max = 250

params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = True
params.minInertiaRatio = Circle_Inertia

detector = cv2.SimpleBlobDetector_create(params)    #Blob 검출

class cap_yolo:
    def yolo(frame, model_label):
        clientSocket = socket() # Open Socket
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

        frame_blurred = cv2.GaussianBlur(dst, Gaussian_ksize, 1)      #가우시안
        frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)    #흑백
        frame_canny = cv2.Canny(frame_gray, canny_threshold_min, canny_threshold_max, apertureSize=3, L2gradient=True)  #캐니 임계

        keypoints = detector.detect(frame_canny)    #검출기

        num = len(keypoints)    #검출 숫자
        readings.append(num)

        # print(num)    # 찍히는 숫자 확인

        if fair == "true" :
            if readings[-1] == readings[-2] == readings[-3] :    #10회 반복해서 같으면 송신
                socketTxData = bytes([76,83,73,83,45,88,71,84,0,0,0,0,160,51,0,0,22,0,0,0,88,0,2,0,0,0,1,0,8,0,37,68,87,48,49,49,48,48,2,0,])                                        
                num_little = num.to_bytes(2, 'little')

                if num != 0:
                    print("num is " + str(num) + " value is " + fair)
                    try:
                        clientSocket = socket(AF_INET, SOCK_STREAM)
                        clientSocket.connect(ADDR)
                        print('Connection PLC Success!')
                        clientSocket.send(socketTxData + num_little)
                    except  Exception as e:
                        print(e)

                clientSocket.close()
                print('close PLC Success!')
                readings.append(0)
                sleep(1)    # PLC는 빠르게 데이터를 받지 못하므로 반드시 sleep 1처리



