# coding=utf-8
import cv2

def detect_face(img):
    #改变图像大小
    #img = cv2.resize(img,(50,50))

    #将测试图像转换为灰度图像，因为opencv人脸检测器需要灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    #加载OpenCV人脸检测分类器Haar
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
 
    #检测多尺度图像，返回值是一张脸部区域信息的列表（x,y,宽,高）
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
 
    # 如果未检测到面部，则返回原始图像
    if (len(faces) == 0):
        return None, None
 
    #目前假设只有一张脸，xy为左上角坐标，wh为矩形的宽高
    (x, y, w, h) = faces[0]
 
    #返回图像的正面部分
    return gray[y:y + w, x:x + h], faces[0]

