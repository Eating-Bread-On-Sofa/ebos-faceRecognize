# coding=utf-8 
import cv2
import os
import numpy as np
import threading
import base64
from flask import Flask,Response
from draw_image import draw_rectangle,draw_text
from image_detect import detect_face
from image_predict import prepare_training_data,predict
from video_camera import VideoCamera
from activemq import json_msg,send_to_topic

app = Flask(__name__)

def recognize():
    #加载测试图像
    camera = VideoCamera()
    success,test_img = camera.get_frame()
    while True:
        while True:
            #test_img = camera.get_frame()
            if not success:
                return("读取不到视频图片")
            m,n = detect_face(test_img)
            if m is not None:
                break
            else:
                success,test_img = camera.get_frame()
        #test_img = cv2.imread("collect/training_data/2/1.jpg")
        #执行预测
        name,predicted_img = predict(test_img)
        base64_data = ""
        if name == "识别失败":
            cv2.imwrite("./failed_recog.jpg",predicted_img)
            with open("./failed_recog.jpg","rb") as f:
                base64_data = base64.b64encode(f.read())
        json_msg(name,base64_data)
        #显示图像
        cv2.imshow("predict", predicted_img)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()


@app.route('/recognize')
def main():
    t1 = threading.Thread(target = recognize)
    t1.setDaemon(True)
    t1.start()
    return "开始识别"

@app.route('/ping')
def ping():
    return "ping success"

if __name__ == '__main__':
    app.run()
