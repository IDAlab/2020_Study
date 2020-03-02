from pyimagesearch.utils.conf import Conf
from imutils.video import VideoStream
from imutils import face_utils
from datetime import datetime
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

def euclidean_dist(ptA, ptB):
    return np.linalg.norm(ptA-ptB)

def eye_aspect_ratio(eye):
    a = euclidean_dist(eye[1],eye[5])
    b = euclidean_dist(eye[2],eye[4])
    c = euclidean_dist(eye[0],eye[3])
    ear = (a+b)/(2.0*c)
    return ear
def mouth_aspect_ratio(mouth):
    a = euclidean_dist(mouth[1],mouth[7])
    b = euclidean_dist(mouth[2],mouth[6])
    c = euclidean_dist(mouth[3],mouth[5])
    d = euclidean_dist(mouth[0],mouth[4])
    mar = (a+b+c)/(2.0*d)
    return mar

ap = argparse.ArgumentParser()
ap.add_argument("-c","--conf",required=True,help="Path to the input configuration file")
args = vars(ap.parse_args())
conf = Conf(args["conf"])
centerX = None
centerY = None
blinkCounter = 0
yawnCounter = 0
alarmOn = False
startTime = None
print("[INFO] loading facial landmark predictor...")
detector = cv2.CascadeClassifier(conf["cascade_path"])
predictor = dlib.shape_predictor(conf["shape_predictor_path"])
(lStart,lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart,rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(mStart,mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]
print("[INFO] starting video stream thread...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if centerX is None and centerY is None:
        (centerX,centerY) = (frame.shape[1] // 2, frame.shape[0] // 2)
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5,minSize=(30,30),flags = cv2.CASCADE_SCALE_IMAGE)

    for rect in rects:
        (x,y,w,h)=rect
        cv2.rectangle(frame, (x,y),(x+w,y+h),(255,0,0),2)

    if len(rects) > 0:
        centerRect = sorted(rects,key=lambda r : abs((r[0]+(r[2]/2)) - centerX) + abs((r[1] + (r[3] /2)) - centerY))[0]
        (x,y,w,h) = centerRect
        rect = dlib.rectangle(int(x),int(y),int(x+w),int(y+h))
        shape = predictor(gray,rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR)/2.0
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame,[leftEyeHull],-1,(0,255,0),1)
        cv2.drawContours(frame,[rightEyeHull],-1,(0,255,0),1)
        if ear < conf["EYE_AR_THRESH"]:
            blinkCounter +=1;
            if blinkCounter >= conf["EYE_AR_CONSEC_FRAMES"]:
                if not alarmOn:
                    alarmOn =True
                    if conf["alarm"]:
                        print("ring!! ring!!")
                cv2.putText(frame,"DROWSINESS ALERT! -eyes",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
        else:
            blinkCounter = 0
            alarmOn = False
        mouth = shape[mStart:mEnd]
        mar = mouth_aspect_ratio(mouth)
        mouthHull = cv2.convexHull(mouth)
        cv2.drawContours;(frame,[mouthHull],-1,(0,0,255),1)
        if mar>conf["MOUTH_AR_THRESH"]:
            yawnCounter += 1
            startTime = datetime.now() if startTime == None else startTime
            if yawnCounter >= conf["YAWN_THRESH_COUNT"] and (datetime.now()-startTime).seconds <= conf["YAWN_THRESH_TIME"]:
                if not alarmOn:
                    alarmOn =True
                    if conf["alarm"]:
                        print("ring!! ring!!")
                cv2.putText(frame,"DROWSINESS ALERT! - yawning",(10,85),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
        elif startTime != None:
            if (datetime.now() - startTime).seconds > conf["YAWN_THRESH_TIME"]:
                yawnCounter = 0
                alarmOn = False
                startTime = None
        cv2.putText(frame,"EAR: {:.3f} MAR: {:.3f}".format(ear,mar),(175,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
    if conf["display"]:
        cv2.imshow("Frame",frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
if conf["display"]:
    cv2.destroyAllWindows()
vs.stop()