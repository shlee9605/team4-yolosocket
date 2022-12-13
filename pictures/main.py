import cv2

camrea = cv2.VideoCapture(1)

if not camrea.isOpened():
    print("Could not open webcam")
    exit()

pic = 0

while camrea.isOpened():
    status, frame = camrea.read()

    cv2.imshow("picture", frame)
    cv2.imwrite("dice"+str(pic)+".jpg", frame)
    pic+=1

    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

camrea.release()
cv2.destroyAllWindows()