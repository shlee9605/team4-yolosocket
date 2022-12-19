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
For Development OS, I used `Windows10`.  
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
  
Because this plugin requires lots of information about naver cloud platform,  
I wrote detailed manual about this plugin in [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#1f80ba301cd74cc6b3f46a7a1b1fffa3).  
  
## Torch

### Installation
This allows you to read csv files in flutter.  

```console
> flutter flutter pub add csv  
```  
  
### Configuration
For this project, You need to setup csv files in your asset folders `C:\Workspace\assets\areas`.  
Move your `csv` files which contains location coordinate data.  
csv file must include information of location name(id), latitude, and longitude.  

Below shows you some of examples of csv contents.  
```
1-1,37.50375605,127.0241095
1-2,37.48276664,127.0349496
1-3,37.48124455,127.0361898
...
```
  
### Usage
Below code shows example how I applied in this project
```dart
class SmokingAreaData {
  //for smoking area
  static List<List<dynamic>>? csvData;

  //read csv data from assets/areas
  static Future<List<List<dynamic>>> processCsv() async {
    var result = await rootBundle.loadString(
      "assets/areas/Seocho_SmokingArea.csv",
    );
    return const CsvToListConverter().convert(result, eol: "\n");
  }

  //return as list of custom marker, using csv data
  static Future<List<AreaType>> markers() async {
    List<AreaType> areas = [];
    csvData = await processCsv();

    //add in area list using which gives you areatype
    for (List<dynamic> lt in csvData!) {
      areas.add(SmokingArea(aid: lt[0], location: LatLng(lt[1], lt[2])));
    }
    
    return areas;
  }
}
```
  
## Flask

### Installation
This allows you to use google mobile ad banner in organized form/widget.  

```console
> flutter flutter pub add google_mobile_ads  
```  
  
I also had to write manual in [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#1f80ba301cd74cc6b3f46a7a1b1fffa3),  
since this plugin also requires lots of information about google cloud platform, firebase, and Admob  
  
  
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
  
## Time, sleep
라이브러리 설치 -비밀번호 암호화, 토큰 관리
  
  
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
  
