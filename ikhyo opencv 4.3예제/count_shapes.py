import argparse
import imutils
import cv2

p="./star.png"
image=cv2.imread(p)
resize=cv2.resize(image,(800,600))
gray=cv2.cvtColor(resize,cv2.COLOR_BGR2GRAY)
Blur=cv2.GaussianBlur(gray,(3,3),0)
edged = cv2.Canny(Blur,50,130)
cv2.imshow("edge",edged)
cnts=cv2.findContours(edged.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)
total=0
for c in cnts:
	cv2.drawContours(resize,[c],-1,(255,255,255),1)
	total+=1
print("[INFO] found {} shapes".format(total))
cv2.imshow("resize",resize)
cv2.waitKey(0)
cv2.destoryAllwindows()

