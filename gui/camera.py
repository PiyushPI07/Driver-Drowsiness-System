import cv2,os,urllib.request
from imutils.video import VideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import datetime
import os
import base64
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    def read(self):
        return self.video.read()
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # faces_detected = face_detection_videocam.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        # for (x, y, w, h) in faces_detected:
            # cv2.rectangle(image, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=2)
        # frame_flip = cv2.flip(image,1)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

class Webcam(object):
    path = os.path.dirname(__file__)
    file_path =     os.path.join(path, "shape_predictor_68_face_landmarks.dat")
    landmarks = dlib.shape_predictor(file_path) #change to absolute path
    face_recognition = dlib.get_frontal_face_detector()
    context= {
        'message': ""
    }
    def __init__(self):
        self.webcam = VideoStream(src=0).start()
        time.sleep(1.0)
        self.sleep_count = 0
        self.max_sleep_count = 30
        self.normal = False
        self.normal_count = 0.0
        self.normal_eye_ratio = 0

    def eye_ratio(self, eye):
        avg_height = (abs(eye[1][1]-eye[5][1])+abs(eye[2][1]-eye[4][1]))/2
        width = abs(eye[0][0]-eye[3][0])
        return avg_height/width

    def stop(self):
        cv2.destroyAllWindows()
    def read(self):
        frame = self.webcam.read()
        frame = imutils.resize(frame, width=450)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        input_frame = img
        now = datetime.datetime.now()
        CurrentTime = now.strftime("%Y-%m-%d %H:%M:%d")
        cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
        while True:
            frame = self.webcam.read()
            frame = imutils.resize(frame, width=450)
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_recognition(img, 0)
            if(not(self.normal) and self.normal_count<47):
                cv2.rectangle(input_frame, (1, 50), (50, 80), (180, 132, 109), -1)
                cv2.putText(
                    input_frame,
                    'ATTENTION PLEASE - Your activities are being logged',
                    (60, 70),
                    self.font,
                    0.5,
                    (0xFF, 0xFF, 0xFF),
                    1,
                    cv2.FONT_HERSHEY_SIMPLEX,
                    )
            for face in faces:
                face_data = face_utils.shape_to_np(self.landmarks(img, face))
                left_eye = face_data[36:42]
                right_eye = face_data[42:48]
                leftEyeHull = cv2.convexHull(left_eye)
                rightEyeHull = cv2.convexHull(right_eye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                eye_avg_ratio = self.eye_ratio(left_eye) + self.eye_ratio(right_eye)/2.0

                if(not(self.normal)):
                    if(self.normal_count < 50):
                        self.normal_eye_ratio = self.normal_eye_ratio+eye_avg_ratio
                    else:
                        self.normal_eye_ratio = self.normal_eye_ratio/self.normal_count
                        self.normal = True
                        cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
                        print(self.normal_eye_ratio)
                self.normal_count+=1
            else:
                    if(self.normal_eye_ratio - eye_avg_ratio > 0.05):
                        self.sleep_count +=1
                        GPA = self.sleep_count/30

                        if(self.sleep_count>self.max_sleep_count):
                            now = datetime.datetime.now()
                            CurrentTime= now.strftime("%Y-%m-%d %H:%M:%S")
                            cv2.putText(frame, "Sleep Detector: " + str(CurrentTime), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0xFF, 0xFF, 0xFF0), 2)
                            cv2.putText(frame, "Sleeping time (seconds):" + str("%6.0f " % GPA), (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0xFF, 0xFF, 0xFF0), 2)
                        if ((GPA > 2) and (GPA < 5)):
                            cv2.putText(frame, "Alert! You should take a rest", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                            # context['message'] = "Alert! You should take a rest"
                        print("Sleeping log - Time: " + str(CurrentTime) + " Duration: " + str("%6.0f" % GPA))
                    else:
                        self.sleep_count = 0
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')