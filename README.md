# 0. Abstract
**Notion : [UVC Team 4 Project Yolo Socket Stream](https://www.notion.so/1d50eee57be542fd8435cf5088dd9936#778988f111d4416abeb34f7d15eb9f94)**  
**This project is about UVC Team Project**  
**This project is to implement Smart Factory Management System.**  
This document only notes how I used Yolo Model & Socket System & Flask to apply  
AI Model & Socket Connection with PLC & Stream on HTTP Server  

I Referenced most of the code from UVC,
Especially On Socket Connection Part.

## Index  

[**1. File Structure**](https://github.com/shlee9605/team4-yolosocket#1-file-structure)  
[**2. Develop Environment**](https://github.com/shlee9605/team4-yolosocket#2-Develop-Environment)  
[**3. Getting Packages**](https://github.com/shlee9605/team4-yolosocket#3-Getting-Packages)  
[**4. Setting Configuration**](https://github.com/team4-yolosocketmd#4-Setting-Configuration)  
[**5. Used Concept**](https://github.com/shlee9605/team4-yolosocket#5-Used-Concept)  
[**6. Usage Example**](https://github.com/shlee9605/team4-yolosocket#6-Usage-Example)  

## Undone Document
  
[**System Link with your DB(database)**](https://github.com/shlee9605/CaMap/blob/Ver0.6/README.md#system-link-with-your-dbdatabase)  
[**etc packages**](https://github.com/shlee9605/CaMap/blob/Ver0.6/README.md#etc)  
[**Used Concept**](https://github.com/shlee9605/CaMap/blob/Ver0.6/README.md#5-Used-Concept)  
[**Usage Example**](https://github.com/shlee9605/CaMap/blob/Ver0.6/README.md#6-Usage-Example)  
  
# 1. File Structure

```
.
└── dev.py			      # Main
    ├── cam.py		    # Socket Sending Camera
    └── stream.py     # Streaming Camera
```

# 2. Develop Environment

For : Windows(anaconda prompt ver3)  
Used : Yolo, OpenCV, Flask, ETC  
**You Must Refer [My Notion(in Kor)](https://www.notion.so/UVC-c36970dd6c884131b159ea837790db94) Together for Plugin Packages Description of This Project**  

## Setup
For Development OS, I used `Windows10(anaconda3)`.  
Then, set your working space for python  
```console
> cd C:\Workspace
```
  
## Installation
You need to set up Yolov5
Checkout [My Notion(in Kor)](https://www.notion.so/1d50eee57be542fd8435cf5088dd9936#38e3ee19b7d34922bc082fc9921ff235) for Installation in Windows  
You can also refer to [Yolov5 documents](https://github.com/ultralytics/yolov5),  
which includes information about [Training Custom Dataset](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data), [Roboflow](https://roboflow.com/?ref=ultralytics)
  
## Activate Anaconda
Create Your Project
```console
> conda create -n yolov5 python=3.9  
> conda activate yolov5  
```
  
## Running Project
You can run your project via commands below

### default(debug Mode)
```console
> python dev.py  
```
  
# 3. Getting Packages

## Packages
```Python
import cv2
import torch
from time import sleep

from threading import Thread
from socket import *  

from flask import Flask  
from flask import Response  
from flask import stream_with_context 
```
  
## OpenCV

### Installation
The following allows you to use OpenCV library, 
which is mainly about vision sensing  

```console
> pip install opencv-python>=4.1.1
```  
  
### Configuration
For this project, You need to setup your own camera.  
Then, you need to check out which camera you are using from **Windows Device Manager**.  
After checking which camera you are using, You can Open your camera through python  
via below code.  
```Python
if cv2.ocl.haveOpenCL() :
    cv2.ocl.setUseOpenCL(True)
print('OpenCL : ', cv2.ocl.haveOpenCL())
webcam = cv2.VideoCapture(0)
```
  
### Usage
After making sure that your camera is opened,  
You can use variety of OpenCV functions.  
Below code is some example of how I used OpenCV in this project
```Python
detector = cv2.SimpleBlobDetector_create(params)    #Detecting Blob
...
imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)     #Making RGB file to BGR for openCV
...
cv2.putText(imgRGB, 'Dice', (dice[0], dice[1]), cv2.FONT_HERSHEY_SIMPLEX, 2,(0, 255, 0), 2) #Putting Text
cv2.rectangle(imgRGB, (dice[0], dice[1]), (dice[2], dice[3]), (0, 0, 255), 3)               #Drawing Rectangle
...
frame_blurred = cv2.GaussianBlur(dst, Gaussian_ksize, 1)      #Gaussian Blur Filter
frame_gray = cv2.cvtColor(frame_blurred, cv2.COLOR_BGR2GRAY)    #Gray Filter
frame_canny = cv2.Canny(frame_gray, canny_threshold_min, canny_threshold_max, apertureSize=3, L2gradient=True)  #Canny Edge
...
```
  
## Torch

### Installation
This allows you to use Torch library, which means that you are now  
available to Use Trained Yolo .pt Model

```console
> pip install torch>=1.7.0
```  
  
### Configuration
To use yolo model and call the trained model successfully,  
You need to specify your yolo model's path

Below Shows how I specify My Yolo&Yolo model
```Python
...
model_label = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/dices5/weights/last.pt', source='local') # Read Train Model
...
```
  
### Usage
After reading yolo model via pytorch, You can use it via returned variable.
```Python
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
```
  
## Flask

### Installation
This allows you to open route server via python.
I used it in this project to stream my Yolo-Applied-Vision.  

```console
> pip install flask>=2.2.2  
```  

### Configuration
To Use Flask Model, You need to setUp both Host and Port.  
Here is the following to setup host and port using flask
  
```Python
...  
app = Flask(__name__)
@app.route('/stream')
def stream():  
...  
app.run(host='0.0.0.0', port=3002)  
```
  
### Usage

  
  
## Thread, Time, Socket

### Installation
This gives you exact coordinates about your location  
  
```console
> flutter flutter pub add geolocator  
```  
  
### Configuration
  Will be updated in Ver 1.0
  
### Usage
  Will be updated in Ver 1.0
  
  
# 4. Setting Configuration
Create your `.gitignore` file in `C:\Workspace`, then setup like below.  
In `C:\Workspace\.gitignore`,  
  
```
.env
assets/
/android/key.properties
/android/app/camap.jks
/android/app/proguard-rules.pro
...       # default .gitignore for flutter  
```
  
## dotenv configuration
  
We have already discuss about using dotenv configuration above.  
Please note [flutter_config](https://github.com/shlee9605/CaMap/blob/Ver0.6/README.md#flutter_config)
  
## assets configuration
  
In `C:\Workspace\pubspec.yaml`,  

**Assets**
```RAML
flutter:
  uses-material-design: true

  assets:
  - assets/markers/ 	#for marker location in csv
  - assets/areas/ 	  #for marker image icon in png
```
  
Then, make assets/markers & assets/areas folder in `C:\Workspace`.  
  
## keystore configuration
  
keystore configuration requires basic knowledge about key signing.
Check out [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#a575498637cf4011b617deda1e9cfd72)  
  
## proguard configuration
  
proguard configuration requires basic knowledge about multidex support.  
Check out either [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#8a23338df33c40a9b3aa377f048ca3b8) or [Google flutter documents](https://docs.flutter.dev/deployment/android#enabling-multidex-support).  
  
  
# 5. Used Concept
  
CRUD구조 같은 거
  
# 6. Usage Example
  
프로그램 예시
  
