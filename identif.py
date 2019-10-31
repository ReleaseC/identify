import cv2
import face_recognition
import os
import oss2
import urllib.request
import requests
import sys
from socketIO_client_nexus import SocketIO, LoggingNamespace
import numpy as np
import glob
import time

starttime = time.time()
def identify_socket():
    print("=====identify_socket======")
    print(url_list)
    uploaddata = {
        "param":{
            "action":"check_face_responds",
            "url":url_list,
            "url_list":url_list,
            "ending":ending
        },
        "from":openid
    }
    try:    
        with SocketIO('101.37.151.52', 3000, LoggingNamespace) as socketIO:
             socketIO.emit('cmd',uploaddata)
             
    except requests.exceptions.ConnectionError as e:
        print("[Warn]Please check your network")
        #check_and_restore_network(momeu_upload_socket())
    except BaseException as e:
        print("momeu_upload_socket error",e)

def oss():
    global url
    global img_name
    global file_name
    img_key =  file_name
    img_path = img_name
    img_key = 'face_reognition/'+img_key
    #img_path = '/media/siiva/F/dlib人脸识别/face_recognition_examples-master/img/img_list/' + img_path
    auth = oss2.Auth('LTAIAHvYCJg3q0sp', 'EOPCMRjjW3mDC8MFV4LSwAMEiMKVny')
    endpoint = 'https://oss-cn-hangzhou.aliyuncs.com'
    img_oss_path = "https://siiva-video-public.oss-cn-hangzhou.aliyuncs.com/" + img_key
    try:
        bucket = oss2.Bucket(auth, endpoint, 'siiva-video-public')
        bucket.put_object_from_file(img_key, img_path)
        print("upload success")
        url = img_oss_path
        url_list.append(url)
    except oss2.exception.NoSuchKey as e:
        print("oss2 no suchkey", e)
    except Exception as e:
        print("upload err",e)
        
def gen_get_length(text):
    for i, letter in enumerate(text):
        yield i

def find_video():
    global url_list
    global img_name
    global file_name
    global ending
    global item_name
    global dets
    url_list = []
    dir_files = "./source_dir"
    dir_files2 = "./target_txtdir"
    #start_timestamp = sys.argv[2] #1565161200000
    #end_timpstamp =  sys.argv[3] #1565168400000

    start_timestamp = "1565080173523"
    end_timpstamp   = "1565099999999"
    f = glob.iglob(r''+dir_files2+'/'+start_timestamp[0:4]+'*')
    f1 = glob.iglob(r''+dir_files2+'/'+start_timestamp[0:4]+'*')
    # read input image      
    file_length = len(list(gen_get_length(f1)))
    testcount = 0
    for index,item in enumerate(f):
        testcount+=1
        txt_item = item.split("/")[-1]
        jgp_item = txt_item[0:13]
        #if(int(item[70:83])>= int(start_timestamp) and int(item[70:83]) <= int(end_timpstamp)):
        if(True):
            #result = indentify(frame)
            try:
                dets= np.loadtxt('/home/siiva/桌面/identifypeople/imagetx1/'+txt_item,delimiter=',')
                result = indentify2()
            except:
                result = False
            #print(item[39:87])
            if result :
                print("识别到了,程序一共找了",testcount,"个","花了",time.time()-starttime,"时间")
                testcount = 0
                file_name = dir_files+"/"+jgp_item + ".jpg"
                print("file_name",file_name)
                img_name = dir_files+"/"+jgp_item + ".jpg"
                oss()
                identify_socket()
        
        else:
            pass

        if isShowFrame:
            cv2.imshow("frame",frame)
            key = cv2.waitKey(1)
            if key == ord('q') or key == 27:
                print('press stop key')
                cap.release()
                cv2.destroyAllWindows()
                exit(1) 
       

        if(index == file_length-1):
            ending = True
            print("ending",ending)            
            identify_socket()
            return 
    
    cap.release()
    sys.exit()

def init_param():
    global Flag
    global isShowFrame
    global user_face_encoding
    global openid
    global url_list
    global ending
    global url_list
    ending = False
    Flag = False
    isShowFrame = False
    url = sys.argv[1]
    url_list = []
    #dowload img init user img
    #url = "https://siiva-video.oss-cn-hangzhou.aliyuncs.com/face/tmp_00d944bc17762da3b7af84837aa740fb22037570b250393d.jpg"
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()),dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    openid = sys.argv[4]
    try:
        image_of_bill = face_recognition.face_locations(image)
        user_face_encoding = face_recognition.face_encodings(image,image_of_bill)[0]
        find_video()
    except:
        print("error")
        ending = True
        print("ending",ending)            
        identify_socket()
        sys.exit(0)
    #test_image1 = face_recognition.load_image_file('/media/siiva/F/换脸/12.jpg')
    #image_of_bill = face_recognition.face_locations(test_image1)
    #user_face_encoding = face_recognition.face_encodings(test_image1, image_of_bill)[0]
    

def indentify2():
    global dets
    # Find faces in test image/media/siiva/F/换脸
    if len(dets) == 128:
        rs = face_recognition.compare_faces([dets], user_face_encoding,tolerance=0.36)
        distance = face_recognition.face_distance([dets],user_face_encoding )
        return rs[0]
    else:    
        for item in dets:
            rs = face_recognition.compare_faces([item], user_face_encoding,tolerance=0.36)
            print(rs)
            distance = face_recognition.face_distance([item],user_face_encoding)
            print(distance)
            if(rs[0]==True):
                print("在视频里")
                return True
                break
        
        return False

def indentify(frame):
    global Flag
    print("===indentify===indentify")
    #test_image = face_recognition.load_image_file(frame)
    test_image = frame

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)
    #distance = face_recognition.face_distance(test_image, face_locations)
    #print(distance)
    # Loop through faces in test image
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      matches = face_recognition.compare_faces(user_face_encoding, face_encoding,tolerance=0.47)
      distance = face_recognition.face_distance(user_face_encoding, face_encoding)
      print("=== all == distance",distance,"img",item_name)
      #print(distance)
      # If match
      if True in matches:
        #print("===true == distance")
        Flag = True
      else:
        Flag = False

    return Flag
  

if __name__ == '__main__':
    init_param()
    
