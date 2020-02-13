from pyimagesearch.notifications.twilionotifier import TwilioNotifier
from pyimagesearch.utils.conf import Conf
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-c","--conf",required=True,help="path to the input configuration file")
args = vars(ap.parse_args())
conf = Conf(args["conf"])
tn= TwilioNotifier(conf);
print("[INFO] sending txt message...")
tn.send("Incomming message from your RPI!")
print("[INFO] txt message sent")