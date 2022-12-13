import cv2
import numpy as np

webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()

    if status:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      # 가우시안
        blr = cv2.GaussianBlur(gray, (0, 0), 1.0)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 15, param1 = 250, param2 = 10, minRadius = 5, maxRadius = 10)
        # dst = frame.copy()

        if circles is not None:
        #     print("not reading")

        # else:
            for i in circles[0]:
                cv2.circle(frame, (int(i[0]), int(i[1])), int(i[2]), (0, 0, 255), 5)

        cv2.imshow("test", frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

