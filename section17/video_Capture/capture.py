import cv2, time

video=cv2.VideoCapture(0)

counter=0
while True:
    check, frame = video.read()
    print(check)
    counter=counter+1
    print(frame)

    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #time.sleep(3)
    cv2.imshow("Capturing", gray_frame)
    key=cv2.waitKey(1)

    if key == ord('q'):
        break
print(counter)
cv2.destroyAllWindows
video.release()
