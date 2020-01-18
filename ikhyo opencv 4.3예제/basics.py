import imutils
import cv2
import os
p="./friends.jpeg"
image=cv2.imread(p)
h,w,d = image.shape
(B,G,R) =image[200,430]
print("width={},hight={},depth={}".format(w,h,d))
print("R={},G={},B={}".format(R,G,B))
resized = cv2.resize(image,(800,600))
cv2.rectangle(resized,(358,132),(480,295),(255,255,255),5)
cv2.putText(resized,"this is my friends",(10,550),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
cv2.imshow("Drowing",resized)
roi = resized[132:295,358:480]
cv2.imshow("ROI",roi)
rotated=imutils.rotate(resized,-45)
cv2.imshow("Rotation",rotated)
blurred =cv2.GaussianBlur(resized,(11,11),0)
cv2.imshow("Blurred",blurred)
cv2.waitKey(0)
cv2.distroyAllwindows()
