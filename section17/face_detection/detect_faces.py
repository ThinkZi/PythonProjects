import cv2

face_cascade=cv2.CascadeClassifier("https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml")

img=cv2.imread("news.jpg")
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces=face_cascade.detectMultiScale(gray_image,scaleFactor=1.1, minNeighbors=10)

for face in faces:
    cv2.rectangle(img,(face[0],face[1]),(face[0]+face[2],face[1]+face[3]),(0,255,0),3)

cv2.imshow("face",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
