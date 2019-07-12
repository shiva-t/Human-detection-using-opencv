# import the necessary packages
from google.cloud import storage
from google.cloud import firestore
from picamera.array import PiRGBArray
from time import sleep
from picamera import PiCamera
import time
import cv2
import numpy as np
import os

def uploadFile(file):
 storage_client = storage.Client()
 bucket = storage_client.get_bucket('video-surv.appspot.com')
 blob = bucket.blob(file)
 print("Uploading..{}" .format(file))
 blob.upload_from_filename("/home/pi/test-pro/diff/"+file)
 
 
def getFlag():
 db = firestore.Client()
 collec = db.collection('switch')
 docs = collec.get()
 for doc in docs:
  flag = doc.get('status')
 return flag
 
face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_frontalface_default.xml')
#eye_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_eye.xml')
#upper_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.3.0/data/haarcascades/haarcascade_upperbody.xml')

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.rotation = 180

camera.resolution = (640,480)
camera.framerate=32
rawCapture = PiRGBArray(camera, size=(640,480))
# allow the camera to warmup
time.sleep(0.5)

init=1
path= '/home/pi/test-pro/Captured'
j=1
k=1
l=1
skip=0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame2 = frame.array
    global init
    if init==1:
        frame1= frame.array
        init=init-1

    d = cv2.absdiff(frame1, frame2)
    grey = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)  # apply gaussian blur
    ret, th = cv2.threshold( blur, 20, 255, cv2.THRESH_BINARY)  #applying threshold
    dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=1 )  #morphological -dilation,np.ones-kernel
    eroded = cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=1 )
    img, c, h = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #adding contours

    for contour in c:
        if cv2.contourArea(contour) < 5000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 3)
        count = cv2.countNonZero(eroded)
        print(count)
        if j<50:
            cv2.imwrite(os.path.join(path , "image%04i.jpg" %j), frame2)
            j += 1

        #imag=cv2.imread('/home/pi/Test/Captured/"image%04i.jpg" %j')
        img=frame2
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(grey, 1.3, 5)
        #up = upper_cascade.detectMultiScale(grey, 1.1 , 3)

        if skip==0:
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #roi_gray = grey[y:y+h, x:x+w]
            #roi_color = img[y:y+h, x:x+w]
            #eyes = eye_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in eyes:
                #cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        #for (x,y,w,h) in low:
           # cv2.rectangle(img, (x,y), (x+w, y+h), (12,150,100),2)

        #for (x,y,w,h) in up:
          #  cv2.rectangle(img, (x,y), (x+w, y+h), (12,150,100),2)
        skip=0

        if k<50:
            cv2.imwrite("/home/pi/test-pro/Face/image%04i.jpg" %k,img)
            k +=1

            original=cv2.imread("/home/pi/test-pro/Captured/image%04i.jpg" %(j-1))
            duplicate=cv2.imread("/home/pi/test-pro/Face/image%04i.jpg" %(k-1))

            if original.shape == duplicate.shape:
                print("The images have same size and channels")
                difference = cv2.subtract(original, duplicate)
                b, g, r = cv2.split(difference)

                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print("The images are completely Equal '{0}' '{1}'".format(j,k) )
                else:
                    print("Not equal,Recording........")
                    cv2.imwrite("/home/pi/test-pro/diff/image%04i.jpg" %(l),duplicate)
                    l+=1
                    #cv2.imshow("Original", original)
                    cv2.imshow("Duplicate", duplicate)
                    camera.start_preview()
                    camera.start_recording("/home/pi/test-pro/diff/video%04i.h264" %(l-1))
                    sleep(10)
                    camera.stop_recording()
                    camera.stop_preview()
                    uploadFile("video%04i.h264"%(l-1))
                    print("Uploaded")
                    skip=1


    cv2.drawContours(frame1, c, -1, (0, 0, 255), 2)


    cv2.imshow("eroded", eroded)
    #cv2.imshow("Original", frame2)
    cv2.imshow("Output", frame1)


    frame1 = frame2
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if j==50:
        j=0
    if k==50:
        k=0
    if l==4:
        l=1

    if key == ord("q"):
        break

cv2.waitKey(0)

cv2.destroyAllWindows()





