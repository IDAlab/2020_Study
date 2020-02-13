from pyimagesearch.notifications.twilionotifier import TwilioNotifier
from pyimagesearch.utils.conf import Conf
from imutils.video import VideoStream
from datetime import datetime
from datetime import date
import numpy as np
import argparse
import imutils
import signal
import time
import cv2
import sys

def signal_handler(sig,frame):
    print("[INFO] you pressed 'ctrl +c'! Closing mail detector application...")
    vs.stop()
    sys.exit(0)
ap=argparse.ArgumentParser()
ap.add_argument("-c","--conf",required=True,help="Path to the input configuration file")
args = vars(ap.parse_args())
conf = Conf(args["conf"])
tn = TwilioNotifier(conf)
mailboxopen = False
notifSent =False
print("[INFO] warming up camera...")
vs=VideoStream(src=0).start()
time.sleep(2.0)
signal.signal(signal.SIGINT,signal_handler)
print("[INFO] Press 'ctrl +c' to exit, or 'q' to quit if you have the display option on...")
while True:
    frame = vs.read()
    frame = imutils.resize(frame,width=200)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mailboxPrevopen = mailboxopen
    mean = np.mean(gray)
    mailboxopen = mean > conf["thresh"]
    if mailboxopen and not mailboxPrevopen:
        startTime=datetime.now()
    elif mailboxPrevopen:
        elapsedTime = (datetime.now()-startTime).seconds
        mailboxLeftopen = elapsedTime > conf["open_threshold_seconds"]
        if mailboxopen and mailboxLeftopen:
            if not notifSent:
                msg="your mailbox at {} has been left open for longer than {} seconds. It is possible that you or the mailman didn't close your mail box.".format(conf["address_id"],conf["open_threshold_seconds"])
                tn.send(msg)
                notifSent=True
        elif not mailboxopen:
            if notifSent:
                notifSent=False
            else:
                endTime = datetime.now()
                totalSeconds = (endTime-startTime).seconds
                dateOpened = date.today().strftime("%A,% B %d %Y")
                msg = "Your mailbox at {} was opened on {} at {} for {} seconds.".format(conf["address_id"],dateOpened,startTime.strftime("%I:%M%p"),totalSeconds)
                tn.send(msg)

    if conf["display"]:
        cv2.imshow("frame",frame)
        key = cv2.waitKey(1) & 0xFF
        if key==ord("q"):
            break

cv2.destroyAllWindows()
vs.stop()