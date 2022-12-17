import cv2
import numpy as np

Circle_Inertia = 0.6
Gaussian_ksize = (7, 7)
canny_threshold_min = 150
canny_threshold_max = 250

params = cv2.SimpleBlobDetector_Params()
params.filterByInertia = True
params.minInertiaRatio = Circle_Inertia

detector = cv2.SimpleBlobDetector_create(params)    #Blob 검출

class stream_yolo : 

    def yolo(frame, model_label):

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
        
        im_with_keypoints = cv2.drawKeypoints(imgRGB, keypoints, np.array([]), (255, 0, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)  #검출
        cv2.putText(im_with_keypoints, "dice : " + str(num) + ", fair : " + fair, (25, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        imgBGR = cv2.cvtColor(im_with_keypoints, cv2.COLOR_RGB2BGR)

        return imgBGR, num, fair

    
