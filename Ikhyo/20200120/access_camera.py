from imutils.video import VideoStream
import imutils
import time
import cv2
print("[INFO] starting video stream...")
vs =VideoStream(src=0).start()
time.sleep(2.0)
while True:
        frame = vs.read()
        frame = imutils.resize(frame,width=400)
        cv2.imshow("Frame",frame)
        key=cv2.waitKey(1) &0xFF
        if key == ord("q"):
                break
cv2.destroyAllWindows()
vs.stop()