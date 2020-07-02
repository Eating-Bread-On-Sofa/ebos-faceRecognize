# coding=utf-8
import cv2
import os

def detect_face(img_path):
    #读取图片
    img = cv2.imread(img_path)

    #改变图像大小
    #img = cv2.resize(img,(50,50))

    #将测试图像转换为灰度图像，因为opencv人脸检测器需要灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    #加载OpenCV人脸检测分类器Haar
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt.xml')
 
    #检测多尺度图像，返回值是一张脸部区域信息的列表（x,y,宽,高）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
 
    # 如果未检测到面部，则删除该图片
    if (len(faces) == 0):
        os.remove(img_path)
