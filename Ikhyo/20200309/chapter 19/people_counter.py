from pyimagesearch.directioncounter import DirectionCounter
from pyimagesearch.centroidtracker import CentriodTraker
from pyimagesearch.trackableobject import TrackableObject
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Value
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2


def write_video(outputPath,writeVideo,frameQueue,W,H):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter(outputPath,fourcc,30,(W,H),True)

    while writeVideo.value or not frameQueue.empty():
        if not frameQueue.empty():
            frame = frameQueue.get()
            writer.write(frame)
    writer.release()

ap = argparse.ArgumentParser()
ap.add_argument("-m","--mode",type=str,required =True, choices=["horizontal","vertical"],help="direction in which people will be moving")
ap.add_argument("-i","--input",type = str, help = "path to optional input video file")
ap.add_argument("-o","--output",type = str, help = "path to optional output video file")
ap.add_argument("-a","--skip-frames",type = int,default=30,help = "# of skip frames between detections")
args = vars(ap.parse_args())
if not args.get("input",False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(2.0)

else:
    print("[INFO] opening video file...")
    vs = cv2.VideoCapture(args["input"])
writerProcess = None
W = None
H = None

ct = CentriodTraker(maxDisappeared =15,maxDistance = 100)
trackers =[]
trackalbeObjects = {}
directionInfo = None
mog = cv2.bgsegm.createBackgroundSubtractorMOG()
fps = FPS().start()

while True:
    frame = vs.read()
    frame = frame[1] if args.get("input",False) else frame
    if args["input"] is not None and frame is None:
        break
    if W is None or H is None:
        (H,W) = frame.shape[:2]
        dc = DirectionCounter(args["mode"],H,W)

    if args["output"] is not None and writerProcess is None:
        writeVideo = Value('i',1)
        frameQueue = Queue()
        writerProcess = Process(target=write_video,args=(args["output"],writeVideo,frameQueue,W,H))
        writerProcess.start()
    rects = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    mask = mog.apply(gray)
    erode = cv2.erode(mask,(7,7),iterations=2)
    cnts = cv2.findContours(erode.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        if cv2.contourArea(c) < 2000:
            continue
        (x,y,w,h) = cv2.boundingRect(c)
        (startX,startY,endX,endY) = (x,y,x+w,y+h)
        rects.append((startX,startY,endX,endY))

    if args["mode"] == "vertical":
        cv2.line(frame,(0,H//2),(W,H//2),(0,255,255),2)
    else:
        cv2.line(frame,(W//2,0),(W//2,H),(0,255,255),2)
    objects = ct.update(rects)
    for(objectID,centroid) in objects.items():
        to = trackalbeObjects.get(objectID,None)
        color = (0,0,255)
        if to is None:
            to = TrackableObject(objectID,centroid)
        else:
            dc.find_direction(to,centroid)
            to.centroids.append(centroid)
            if not to.counted:
                directionInfo = dc.count_object(to,centroid)
            else:
                color = (0,255,0)
        trackalbeObjects[objectID] = to
        text = "ID {}".format(objectID)
        cv2.putText(frame,text,(centroid[0]-10,centroid[1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
        cv2.circle(frame,(centroid[0],centroid[1]),4,color,-1)
    if directionInfo is not None:
        for(i,(k,v)) in enumerate(directionInfo):
            text = "{}:{}".format(k,v)
            cv2.putText(frame,text,(10,H-((i*20)+20)),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255),2)

    if writerProcess is not None:
        frameQueue.put(frame)
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
if writerProcess is not None:
    writeVideo.value = 0
    writerProcess.join()
if not args.get("input",False):
    vs.stop
else:
    vs.release()
cv2.destroyAllWindows()