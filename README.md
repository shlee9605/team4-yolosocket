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
├── dev.py			      # Main
│   ├── cam.py		    # Socket Sending Camera
│   ├── stream.py     # Streaming Camera
```

# 2. Develop Environment

For : Windows
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

### default(release)
```console
> flutter run
> flutter run --release
```
  
If null safety error occurs,
```console
> flutter run --no-sound-null-safety
> flutter run --release --no-sound-null-safety
```
  
### Debug
In debugging mode,  

```console
> flutter run --debug
```
  
If null safety error occurs,
```console
> flutter run --debug --no-sound-null-safety
```

### Build
To publish your project, You need to build your project first.  
You can build your project through commands below.  
You can find your appbundle here : **`C:\Workspace\build\app\outputs\bundle\release`**  
*(Running flutter build defaults to a release build.)*

```console
> flutter build appbundle
> flutter build appbundle --release
> flutter build appbundle --debug
```  
  
If null safety error occurs,
```console
> flutter build appbundle --no-sound-null-safety
> flutter build appbundle --release --no-sound-null-safety
> flutter build appbundle --debug --no-sound-null-safety
```  
  
## System Link with your DB(database)
will be updated in ver 2.0  
  
# 3. Getting Packages
In `C:\Workspace\pubspec.yaml`,  

**Packages**
```RAML
dependencies:
  flutter:
    sdk: flutter

  cupertino_icons: ^1.0.2
  flutter_config: ^1.0.8					#for dotenv
  naver_map_plugin: ^0.9.6 					#for naver map
    # git: https://github.com/LBSTECH/naver_map_plugin.git	#for latest version of naver map
  csv: ^5.0.0 							#for reading csv
  google_mobile_ads: ^2.3.0 					#for google ad
  geolocator: ^8.2.1  
```
  
## cupertino_icons

### Installation
The following adds the Cupertino Icons font to your application.  
Use with the CupertinoIcons class for iOS style icons.  

```console
> flutter flutter pub add cupertino_icons  
```  
  
## flutter_config

### Installation
This allows you to use `.env` files. 

```console
> flutter flutter pub add flutter_config  
```  
  
### Configuration
For this project, You need to setup variables below in your `C:\Workspace\.env`.  
Create `.env` file in your `C:\Workspace`, then setup like below.  
*You must get your ID's from cloud platform first.*  
```
YOUR_CLIENT_ID_HERE = "Naver Client ID"
YOUR_APPLICATION_ID_HERE = "Google Admob Application ID"
```
  
### Usage
After setting up your `.env`, we will use them in `C:\Workspace\android\app\src\main\AndroidManifest.xml`  
```xml
...
 <application
        android:label="CaMap"
        android:name="${applicationName}"
        android:icon="@mipmap/camap_icon">
        <meta-data
            android:name="com.naver.maps.map.CLIENT_ID" 
            android:value="@string/YOUR_CLIENT_ID_HERE" />
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="@string/YOUR_APPLICATION_ID_HERE" />
        <activity
...
```
  
## naver_map_plugin

### Installation
This allows you to use Naver API via naver_map_plugin.  

```console
> flutter flutter pub add naver_map_plugin  
```  
  
Because this plugin requires lots of information about naver cloud platform,  
I wrote detailed manual about this plugin in [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#1f80ba301cd74cc6b3f46a7a1b1fffa3).  
  
## csv

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
  
## google_mobile_ads

### Installation
This allows you to use google mobile ad banner in organized form/widget.  

```console
> flutter flutter pub add google_mobile_ads  
```  
  
I also had to write manual in [My Notion(in Kor)](https://www.notion.so/shlee9605/959ac634936b4a96be20363bc153f53e#1f80ba301cd74cc6b3f46a7a1b1fffa3),  
since this plugin also requires lots of information about google cloud platform, firebase, and Admob  
  
  
## geolocator

### Installation
This gives you exact coordinates about your location  
  
```console
> flutter flutter pub add geolocator  
```  
  
### Configuration
  Will be updated in Ver 1.0
  
### Usage
  Will be updated in Ver 1.0
  
## etc
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
  
