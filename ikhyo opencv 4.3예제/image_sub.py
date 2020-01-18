import numpy as np
import imutils
import cv2

p="./bg.jpeg"
bg=cv2.imread(p)
p="./fg.jpeg"
fg=cv2.imread(p)
bggray=cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
fggray=cv2.cvtColor(fg,cv2.COLOR_BGR2GRAY)
sub=bggray.astype("int32")-fggray.astype("int32")
sub=np.absolute(sub).astype("uint8")
thresh=cv2.threshold(sub,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
thresh=cv2.erode(thresh,None,iterations=1)
thresh=cv2.dilate(thresh,None,iterations=1)
cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
(minX,minY)=(np.inf,np.inf)
(maxX,maxY)=(-np.inf,-np.inf)
for c in cnts:
	(x,y,w,h)=cv2.boundingRect(c)
	minX=min(minX,x)
	minY=min(minY,y)
	maxX=max(maxX,x+w-1)
	maxY=max(maxY,y+h-1)
cv2.rectangle(fg,(minX,minY),(maxX,maxY),(0,255,0),2)
cv2.imshow("Output",fg)
cv2.waitKey(0)
cv2.destroyAllwindows()

