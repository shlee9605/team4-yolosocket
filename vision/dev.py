import cv2
import torch
from time import sleep

from threading import Thread

from flask import Flask
from flask import Response
from flask import stream_with_context

from lib.stream import stream_yolo
from lib.cam import cap_yolo

if cv2.ocl.haveOpenCL() :
    cv2.ocl.setUseOpenCL(True)
print('OpenCL : ', cv2.ocl.haveOpenCL())

model_label = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/dices5/weights/last.pt', source='local') # Read Train Model
webcam = cv2.VideoCapture(0)
if not webcam.isOpened():   # Catch Error
    print("Could not open webcam")
    exit()

def yolo():
    while webcam.isOpened():
        status, frame = webcam.read()   # Read Cam

        if status:
            cap_yolo.yolo(frame, model_label)

def server():
    app = Flask(__name__)
    @app.route('/stream')
    def stream():    
        try :
            
            return Response(
                stream_with_context( hello() ),
                mimetype='multipart/x-mixed-replace; boundary=frame' )
            
        except Exception as e :
            
            print('stream error : ',str(e))

    def hello():
        readings = [-1, -1]
        try : 
            while webcam.isOpened():
                success, frame = webcam.read()
                if not success:
                    break
                else:
                    frame, num, fair= stream_yolo.yolo(frame, model_label)
                    readings.append(num)
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    if readings[-1] == readings[-2] == readings[-3] and readings[-1] != 0 and fair == "true":
                        sleep(1)
            
        except GeneratorExit :
            print( 'disconnected stream' )


    app.run(host='0.0.0.0', port=3002)

t=Thread(target=server, daemon=True)
t.start()

yolo()

webcam.release()
cv2.destroyAllWindows()
