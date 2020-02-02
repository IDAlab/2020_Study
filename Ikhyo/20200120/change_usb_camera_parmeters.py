from imutils.video import VideoStream
import cv2
import time

def toggle_autofocus(vs,autofocus=True):
    vs.stream.set(cv2.CAP_PROP_AUTOFOCUS,1 if autofocus else 0)
    print("[INFO] actual autofocus has been set to {}".format("ON" if autofocus else "OFF"))
    actualAutofocus = vs.stream.get(cv2.CAP_PROP_AUTOFOCUS)
    print("[INFO] actual autofocus {}".format(actualAutofocus))

def toggle_auto_whitebalance(vs,autowb=True):
    vs.stream.set(cv2.CAP_PROP_AUTO_WB,1 if autowb else 0)
    print("[INFO] auto white balance has been set to {}".format("ON" if autowb else "OFF"))
    actualAutoWhitebalance = vs.stream.get(cv2.CAP_PROP_AUTO_WB)
    print("[INFO] actual auto white balance {}".format(actualAutoWhitebalance))

def set_zoom(vs,zoom=0):
    vs.stream.set(cv2.CAP_PROP_ZOOM,zoom)
    print("[INFO] zoom has been set to {}".format(zoom))
    actualZoom = vs.stream.get(cv2.CAP_PROP_ZOOM)
    print("[INFO] actual zoom {}".format(actualZoom))

vs = VideoStream(src=0).start()
time.sleep(2.0)
autofocus=True
autowb = True
zoom = 0
while True :
    frame = vs.read()
    cv2.imshow('Frame',frame)
    key=cv2.waitKey(1)
    if key == ord("q"):
        break
    elif key == ord("f"):
        autofocus = not autofocus
        toggle_autofocus(vs,autofocus)
    elif key == ord("w"):
        autowb = not autowb
        toggle_auto_whitebalance(vs,autowb)
    elif key == ord("i"):
        zoom +=1
        set_zoom(vs,zoom)
    elif key == ord("o"):
        zoom-=1
        set_zoom(vs,zoom)

toggle_autofocus(vs,1)
toggle_auto_whitebalance(vs,1)
set_zoom(vs,100)
vs.stop()
cv2.destroyAllWindows()
