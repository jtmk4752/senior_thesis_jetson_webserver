import face_recognition
import cv2
import cupy as cp
import json
import os


class FaceRecognition():

    camSet=' tcpclientsrc host=192.168.0.2 port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1296)+', height='+str(730)+',format=BGR ! appsink  drop=true sync=false '
    #camSet='  udpsrc port=8554 ! gdpdepay ! rtph264depay ! h264parse ! nvv4l2decoder  ! nvvidconv flip-method='+str(0)+' ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw, width='+str(1296)+', height='+str(730)+',format=BGR ! appsink  drop=true sync=false '
    video_capture = cv2.VideoCapture(camSet)

    known_face_encodings = []
    known_face_names = []
    dir = "./img_data"

    # Initialize some variables
    face_locations = []
    face_encodings = []
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
    

    def run(self):
        # Grab a single frame of video
        ret, frame = self.video_capture.read()

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
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

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

                #print(name)
                return name


if __name__ == "__main__":
    while True:
        print(FaceRecognition().run())
