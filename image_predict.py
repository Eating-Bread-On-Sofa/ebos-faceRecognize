# coding=utf-8
import cv2
import numpy as np
import os
from image_detect import detect_face
from draw_image import draw_rectangle,draw_text
# 该函数将读取所有的训练图像，从每个图像检测人脸并将返回两个相同大小的列表，分别为脸部信息和标签
def prepare_training_data(data_folder_path):
    # 获取数据文件夹中的目录（每个主题的一个目录）
    dirs = os.listdir(data_folder_path)

    # 两个列表分别保存所有的脸部和标签
    faces = []
    labels = []

    # 浏览每个目录并访问其中的图像
    for dir_name in dirs:
        # dir_name(str类型)即标签
        label = int(dir_name)
        # 建立包含当前主题主题图像的目录路径
        subject_dir_path = data_folder_path + "/" + dir_name
        # 获取给定主题目录内的图像名称
        subject_images_names = os.listdir(subject_dir_path)

        # 浏览每张图片并检测脸部，然后将脸部信息添加到脸部列表faces[]
        for image_name in subject_images_names:
            # 建立图像路径
            image_path = subject_dir_path + "/" + image_name
            # 读取图像
            image = cv2.imread(image_path)
            # 显示图像0.1s
            #cv2.imshow("Training on image...", image)
            #cv2.waitKey(100)

            # 检测脸部
            face, rect = detect_face(image)
            # 我们忽略未检测到的脸部
            if face is not None:
                #将脸添加到脸部列表并添加相应的标签
                faces.append(face)
                labels.append(label)

    #cv2.waitKey(1)
    #cv2.destroyAllWindows()
    #最终返回值为人脸和标签列表
    #print(face)
    #print(labels)
    return faces, labels

def predict(test_img):
    #生成图像的副本，这样就能保留原始图像
    img = test_img.copy()
    #检测人脸
    face, rect = detect_face(img)
    if face is None:
        print("no face")
        return img
    #创建人脸识别器
    faces, labels = prepare_training_data("collect/training_data")
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    #预测人脸
    label = face_recognizer.predict(face)
    error = "识别失败"
    if label[1]>=60:
        return error,img
    print(label)
    subjects = ["mom", "dad","son"]
    # 获取由人脸识别器返回的相应标签的名称
    label_text = subjects[label[0]]
 
    # 在检测到的脸部周围画一个矩形
    draw_rectangle(img, rect)
    # 标出预测的名字
    draw_text(img, label_text, rect[0], rect[1] - 5)
    #返回预测的图像
    return label_text,img
