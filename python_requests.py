# -*- coding: utf-8 -*-
import cv2
import json
import base64

img = cv2.imread("/home/siiva/桌面/identifi/301003094.jpg")
#res = {"image": str().encode('base64')}  # img是ndarray，无法直接用base64编码，否则会报错
#res = {"image": str(img.tolist()).encode('base64')} 
imgbase64 = base64.b64encode(str(img.tolist()).encode('ascii'))  # b'eW91ciBuYW1l'
res = {"image": str(imgbase64)} 

import requests

#_ = requests.post("http://192.168.1.111:8081/frame", json=res)    # 比如这里/http://192.168.1.112:8081/frame
print("send")
_ = requests.post("http://192.168.1.190:8081/face_extract", data=json.dumps(res))  # 如果服务器端获取的方式为data 
