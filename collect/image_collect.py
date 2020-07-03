# coding=utf-8
import os
import zipfile
import threading
import pymongo
from image_confirm import detect_face
from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
def unzip_file(zip_src, dst_dir):
    """
    解压zip文件
    :param zip_src: zip文件的全路径
    :param dst_dir: 要解压到的目的文件夹
    :return:
    """
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, "r")
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        return "请上传zip类型压缩文件"

def sort():

    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['imgdb']
    mycol = mydb["imgdata"]
    num = 0
    for x in mycol.find():
        if num <= x['num']:
            num = num + 1
    return num

def detect(target_path,file_name,num):
    for dir_name in os.listdir(target_path):
        dir_path = os.path.join(target_path,dir_name)
        for img in os.listdir(dir_path): 
            img_path = os.path.join(dir_path,img)
            detect_face(img_path,file_name,num)


@app.route("/upload", methods=["POST"])
def upload():
    obj = request.files.get("file") 
    # 检查上传文件的后缀名是否为zip
    ret_list = obj.filename.rsplit(".", 1)
    if len(ret_list) != 2:
        return "请上传zip类型压缩文件"
    if ret_list[1] != "zip":
        return "请上传zip类型压缩文件"

    # 先保存压缩文件到本地，再对其进行解压，然后删除压缩文件
    file_path = os.path.join(BASE_DIR, "training_data", obj.filename)  # 上传的文件保存到的路径
    obj.save(file_path)
    target_path = os.path.join(BASE_DIR, "training_data")  # 解压后的文件保存到的路径
    ret = unzip_file(file_path, target_path)
    os.remove(file_path)  # 删除文件
    if ret:
        return ret
    num = sort()
    t1 = threading.Thread(target = detect,args=(target_path,ret_list[0],num))
    t1.setDaemon(True)
    t1.start()
    return "上传成功"

app.run(host='0.0.0.0',port=5000)
