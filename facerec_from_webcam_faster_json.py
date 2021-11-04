import face_recognition
import cv2
import cupy as cp
import json
import os
import time
import lmdb
import json


class FaceRecognition():

    camSet=' tcpclientsrc host=192.168.0.2 port=8554 ! gdpdepay ! rtph264depay ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1024)+', height='+str(768)+',format=BGR ! appsink  drop=true sync=false '
    #camSet='  udpsrc port=8554 ! gdpdepay ! rtph264depay ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1024)+', height='+str(768)+',format=BGR ! appsink  drop=true sync=false '
    video_capture = cv2.VideoCapture(camSet)

    known_face_encodings = []
    known_face_names = []
    dir = "./img_data"

    # Initialize some variables
    process_this_frame = True

    def __init__(self):
       self.read()

    def read(self):
        for filename in os.listdir(self.dir):
            f = open(self.dir + "/" + filename ,"r")
            json_data = json.load(f)
            name = json_data["name"]
            self.known_face_names.append(name)
            enc_data = json_data["data"]
            self.known_face_encodings.append(enc_data)
            print("read data")

    def run(self):
        # Grab a single frame of video
        ret, frame = self.video_capture.read()

        print(frame)

        if frame.any():
            pass
        else:
            print("no video")

        face_locations = []
        face_encodings = []
        # Resize frame of video to 1/4 size for faster face recognition processing
        img_gpu_src = cv2.cuda_GpuMat()
        img_gpu_dst = cv2.cuda_GpuMat()

        img_gpu_src.upload(frame)
        img_gpu_dst = cv2.cuda.resize(img_gpu_src,(0,0), fx=0.25, fy=0.25)
        small_frame = img_gpu_dst.download()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = None

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                face_distances_gpu = cp.asarray(face_distances)

                best_match_index_gpu = cp.argmin(face_distances_gpu)
                best_match_index = cp.asnumpy(best_match_index_gpu)

                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    
                return name

env = lmdb.Environment("./dbbook")

def lmdb_search(name):
    data=[]

    with env.begin() as txn:
        cur = txn.cursor()
        for _,value in cur:
            d=json.loads(value.decode("utf8"))
            data.append(d)

        for d in data:
            if d["Name"] == name:
                return d["IP"]



if __name__ == "__main__":
    
    FR=FaceRecognition()
    while True:
#        name = FaceRecognition().run()
        name=FR.run()
        if name :
            
            print("Name:",name,"IP:",lmdb_search(name))
            time.sleep(0.5)
