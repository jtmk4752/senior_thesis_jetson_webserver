import face_recognition
import cv2
import numpy as np
import json

import os
import time
import lmdb
from client import SocketClient


RaspiW_IP = "192.168.200.2"
RaspiWH_IP = "192.168.200."
PORT = 9979

camSet2=" tcpclientsrc host="+RaspiW_IP+" port=8554 ! gdpdepay ! rtph264depay ! nvv4l2decoder  ! nvvidconv flip-method="+str(0)+" ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width="+str(1024)+", height="+str(768)+",format=BGR ! appsink  drop=true sync=false "

video_capture = cv2.VideoCapture(camSet2)

while not video_capture.isOpened():
    video_capture = cv2.VideoCapture(camSet2)

dir = "./img_data"
known_face_encodings = []
known_face_names = []

face_locations = []
face_encodings = []

env = lmdb.Environment("./dbbook")


def lmdb_IP_search(name):
    data=[]

    with env.begin() as txn:
        cur = txn.cursor()
        for _,value in cur:
            d=json.loads(value.decode("utf8"))
            data.append(d)

        for d in data:
            if d["Name"] == name:
                return d["IP"]

def rasp_communicate(switch):
    client_W = SocketClient(RaspiW_IP, PORT)
    client_W.connect() # はじめの1回だけソケットをオープン
    if switch: #True->USB connected
        client_W.send_rcv(True)
    else: #False -> USB disconnected
        client_W.send_rcv(False)
    client_W.socket.close()

for filename in os.listdir(dir):
    f = open(dir + "/" + filename, "r")
    json_data = json.load(f)
    name = json_data["name"]
    known_face_names.append(name)
    enc_data = json_data["data"]
    known_face_encodings.append(enc_data)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding in face_encodings:

        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = ""

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        if name :
            IP=RaspiWH_IP+lmdb_IP_search(name)
            print("Name:", name, "IP:", IP)

            client_WH = SocketClient(IP,PORT)
            client_WH.connect()
            current_data = round(client_WH.send_rcv(True))
            print("current: ",current_data)
            client_WH.socket.close()

            if current_data > 1 :
                rasp_communicate(True)
            else :
                rasp_communicate(False)

            time.sleep(1)

# Release handle to the webcam
video_capture.release()