from pyimagesearch.keyclipwriter import KeyClipWriter
from pyimagesearch.utils.conf import Conf
from imutils.video import VideoStream
import numpy as np
import argparse
import datetime
import imutils
import signal
import time
import sys
import cv2
import os
def siganl_handler(sig,frame):
    print("\n[INFO] you pressed 'ctrl +c'!")
    print ("[INFO] your files are saved in the '{}' directory".format(conf["output_path"]))
    if kcw.recording:
        kcw.finish()
    sys.exit(0)
ap = argparse.ArgumentParser()
ap.add_argument("-c","--conf",required=True,help="path to the JSON configuration file")
ap.add_argument("-v","--video",type=str,help="path to optional input video file")
args =vars(ap.parse_args())
conf = Conf(args["conf"])
if not args.get("video",False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(3.0)
else:
    print("[INFO] opening video file '{}'".format(args["video"]))
    vs=cv2.VideoCapture(args["video"])
OPENCV_BG_SUBTRACTORS = {
    "CNT": cv2.bgsegm.createBackgroundSubtractorCNT,
    "GMG": cv2.bgsegm.createBackgroundSubtractorGMG,
    "MOG": cv2.bgsegm.createBackgroundSubtractorMOG,
    "GSOC": cv2.bgsegm.createBackgroundSubtractorGSOC,
    "LSBP": cv2.bgsegm.createBackgroundSubtractorLSBP
}
fgbg= OPENCV_BG_SUBTRACTORS[conf["bg_sub"]]()
eKernel = np.ones(tuple(conf["erode"]["kernel"]),"uint8")
dKernel = np.ones(tuple(conf["dilate"]["kernel"]),"uint8")
kcw = KeyClipWriter(bufSize=conf["keyclipwriter_buffersize"])
framesWithoutMotion = 0
framesSinceSnap=0
signal.signal(signal.SIGINT,siganl_handler)
images = " and images..." if conf["write_snaps"] else "..."
print("[INFO] detecting motion and storing videos{}".format(images))
x=0
y=0
rx=0
ry=0
radius=0
while True:
    fullFrame = vs.read()
    if fullFrame is None:
        break;
    fullFrame = fullFrame[1] if args.get("video",False) else fullFrame
    framesSinceSnap +=1
    frame = imutils.resize(fullFrame,width=500)
    mask = fgbg.apply(frame)
    mask = cv2.erode(mask,eKernel,iterations=conf["erode"]["iterations"])
    mask = cv2.dilate(mask,dKernel,iterations=conf["dilate"]["iterations"])
    cnts= cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    motionThisFrame = False
    for c in cnts:
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        (rx,ry,rw,rh) = cv2.boundingRect(c)
        (x,y,radius) = [int(v) for v in (x,y,radius)]
    if radius < conf["min_radius"]:
        continue
    timestamp = datetime.datetime.now()
    timestring = timestamp.strftime("%Y%m%d-%H%M%S")

    motionThisFrame = True
    framesWithoutMotions = 0

    if conf["annotate"]:
        cv2.circle(frame,(x,y),radius,(0,0,255),2)
        cv2.rectangle(frame,(rx,ry),(rx+ry,ry+rh),(0,255,0),2)
        writeFrame = framesSinceSnap >= conf["frames_between_snaps"]

        if conf["write_snaps"] and writeFrame:
            snapPath = os.path.sep.join([conf["output_path"],timestring])
            cv2.imwrite(snapPath + ".jpg",fullFrame)
            framesSinceSnap = 0

        if not kcw.recording:
            videoPath = os.path.sep.join([conf["output_path"],timestring])
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            #fourcc = cv2.VideoWriter_fourcc(*conf["codec"])
            kcw.start("{}.avi".format(videoPath),fourcc,conf["fps"])
    if not motionThisFrame:
        framesWithoutMotion += 1
    kcw.update(frame)
    noMotion = framesWithoutMotion >= conf["keyclipwriter_buffersize"]
    if kcw.recording and noMotion:
        kcw.finish()
    if conf["display"]:
        cv2.imshow("Frame",frame)
        key=cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
if kcw.recording:
    kcw.finish()
print(cnts)
vs.stop() if not args.get("video",False) else vs.release()
