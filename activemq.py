# coding=utf-8
import stomp
import json

__topic_name = '/topic/notice'
__host = '192.168.0.104'
__port = 61613
__user = 'admin'
__password = 'admin'

def send_to_topic(msg):
    conn1 = stomp.Connection10([(__host, __port)])
    conn1.start()
    conn1.connect(__user, __password, wait=True)
    conn1.send(__topic_name,msg)

def json_msg(name,data):
    msg = '{'+'"type"'+':'+'"name"'+','+'"message"'+':'+'"'+name+'"'+','+'"source"'+':'+'"face_recognize"'+','+'"img"'+':'+'"'+data+'"'+'}'
    print msg
    send_to_topic(msg)

