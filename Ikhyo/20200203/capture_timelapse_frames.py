from imutils.video import VideoStream
from datetime import datetime
import argparse
import signal
import time
import cv2
import sys
import os

def signal_handler(sig,frame):
        print("[INFO] You pressed 'ctrl + c'! Your pictures are saved in the output directory tou specified...")
        sys.exit(0)
ap = argparse.ArgumentParser()
ap.add_argument("-o","--output",required=True,help="Path to the output directory")
ap.add_argument("-d","--delay",type=float,default=5.0,help="Delay in seconds between frames captured")
ap.add_argument("-dp","--display",type=int,default=0,help="boolean used to indicate if frames should be displayed")
args = vars(ap.parse_args())
outputDir = os.path.join(args["output"],datetime.now().strftime("%Y-%m-%d-%H%M"))
os.makedirs(outputDir)
print("[INFO] warming up camera...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True, resolution=(1920,1280),framerate=30).start()
time.sleep(2.0)
count = 0
signal.signal(signal.SIGINT,signal_handler)
print("[INFO] press 'cntl + c' to exit , or 'q' to quit if you have the display option on...")
while True:
        frame = vs.read()
        ts = datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame,ts,(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
        filename = "{}.jpg".format(str(count).zfill(16))
        cv2.imwrite(os.path.join(outputDir,filename),frame)
        if args["display"]:
                cv2.imshow("frame",frame)
                key = cv2.waitKey(1) & 0xFF
                if key== ord("q"):
                        break;
                count+=1
                time.sleep(args["delay"])
print("[INFO] cleaning up...")
if args["display"]:
        cv2.destroyAllWindows()
vs.stop()

