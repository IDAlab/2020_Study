import cv2

p="./friends.jpeg"
image=cv2.imread(p)
resize=cv2.resize(image,(1024,768))
gray=cv2.cvtColor(resize,cv2.COLOR_BGR2GRAY)
detector=cv2.CascadeClassifier('haarcascade_frontface.xml')
rects=detector.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=9,minSize=(40,40),flags=cv2.CASCADE_SCALE_IMAGE)
print("[INFO] detect {} faces".format(len(rects)))
for(x,y,w,h) in rects:
	cv2.rectangle(resize,(x,y),(x+w,y+h),(0,255,0),2)
cv2.imshow("FACES",resize)
cv2.waitKey(0)
cv2.distroyAllwindows()
