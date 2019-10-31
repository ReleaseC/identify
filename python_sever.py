# -*- coding: utf-8 -*-
import face_recognition
from PIL import Image, ImageDraw
from flask import jsonify,request, Flask
import json
import numpy as np
import time
import cv2
import os
app = Flask(__name__)
import cv2
import base64
@app.route("/face_extract", methods=['POST'])
def get_frame():
    face_database = []
     # 获取推过来的json，也可以用data然后转换成json
    try:
        #res = request.json 
        res = json.loads(request.data)
        if(res["image"]) == "" or res["image"] == None:
            return jsonify({"code":3,"msg":"图片资源为空"})
        str_decode = base64.b64decode(res["image"])
        nparr = np.fromstring(str_decode,np.uint8)
        img_restore = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    except BaseException:
        return jsonify({"code":1,"msg":"图片格式不正确，请传入base64"})

    timestamp = time.time()
    img_name = "./source_dir/"+str(int(timestamp)) +".jpg"
    cv2.imwrite(img_name, img_restore)
    test_image1 = face_recognition.load_image_file(img_name)
    face_locations1 = face_recognition.face_locations(test_image1)
    face_encodings1 = face_recognition.face_encodings(test_image1, face_locations1)

    for(top, right, bottom, left), face_encoding in zip(face_locations1, face_encodings1):
        face_database.append(face_encoding)
            
    print("face_database",face_database==[])
    
    if face_database == []:
        np.savetxt("./target_txtdir/"+str(int(timestamp))+".txt", face_database,fmt='%f',delimiter=',')   
        return jsonify({"code":2,"msg":"没有识别到人脸"})
    else:
        np.savetxt("./target_txtdir/"+str(int(timestamp))+".txt", face_database,fmt='%f',delimiter=',')
        return jsonify({"code":0,"msg":"添加成功"})

if __name__ == "__main__":
    app.run("192.168.1.190", port=8081)  #端口为8081
