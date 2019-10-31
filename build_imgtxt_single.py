import face_recognition
from PIL import Image, ImageDraw
import time
import cv2
import numpy as np
import os
print("start")
start_time = time.time()
face_database = []
#300*400
listdir = "./target_dir"

#读取生成的txt文档
for item in os.listdir(listdir):
    item = "1565070074548.jpg"
    test_image1 = face_recognition.load_image_file("/home/siiva/桌面/identifypeople/img_lis1/"+item)
    # Find faces in test image/media/siiva/F/换脸
    face_locations1 = face_recognition.face_locations(test_image1)
    face_encodings1 = face_recognition.face_encodings(test_image1, face_locations1)
    
    for(top, right, bottom, left), face_encoding in zip(face_locations1, face_encodings1):
        face_database.append(face_encoding)
       
    print("write",len(face_database),"item",str(item)[0:13]) 
    np.savetxt("/home/siiva/桌面/identifypeople/imagetx1/"+str(item)[0:13]+".txt", face_database,fmt='%f',delimiter=',')
    face_database = []
    print("===down===")
    break
    



  
