import cv2
import torch
import matplotlib.pyplot as plt

model_label = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/dices5/weights/last.pt', source='local')  
# model_label = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/exp/weights/best.pt', source='local')  

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model_label(imgRGB)
        results = results.pandas().xyxy[0][['name','xmin','ymin','xmax','ymax']]

        dice = False
        cup = False

        for num, i in enumerate(results.values):
            if i[0] == 'Dice' and dice is False :
                cv2.putText(imgRGB, i[0], ((int(i[1]), int(i[2]))), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 3)
                cv2.rectangle(imgRGB, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)
                dice = True

            if i[0] == 'Cup' and cup is False :
                # print(i[0], num, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])))
                cv2.putText(imgRGB, i[0], ((int(i[1]), int(i[2]))), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 3)
                cv2.rectangle(imgRGB, (int(i[1]), int(i[2])), (int(i[3]), int(i[4])), (0, 0, 255), 3)
                cup = True

        # cv2.imread는 BGR로 불러오므로 plt를 이용하려면 RGB로 바꿔줘야 함
        # plt.imshow("test1", imgRGB)
        # plt.show()
        imgBGR = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
        cv2.imshow("test2", imgBGR)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()


