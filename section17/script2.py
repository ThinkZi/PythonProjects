from os import listdir
from os.path import isfile, join
import cv2

mypath=r"C:/Users/hzoghi/Documents/Repos/PythonProjects/section17/sample-images"
destinationPath=r"C:/Users/hzoghi/Documents/Repos/PythonProjects/section17/sample-images/resized_images"
filenames=[f for f in listdir(mypath) if isfile(join(mypath,f))]
print(filenames)

for f in filenames:
    img=cv2.imread(join(mypath,f),1)
    resized_image=cv2.resize(img,(100,100))
    cv2.imwrite(join(destinationPath,"resized_" + f),resized_image)
