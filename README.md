# Human-detection-using-opencv

Implementation of home surveillance including human detection and automated app based notification on Raspberry Pi. 
Designed a home surveillance system using Raspberry Pi and Open CV library. The system performs human detection and sends an alert to 
an android application installed on the user's phone. Also, the video is recorded and uploaded on the cloud database.

Implementation details of Project (Image processing part):

The following is the sequence of steps implemented in the python code to detect the presence of human and start recording video:

● Capture an image frame using PiCamera
For Motion detection:
● Subtract the current frame from the frame of previous iteration (in first iteration these frames can be identical). 
The subtraction helps to find the motion if any.

● Perform basic image processing techniques on the difference image so as to improve the detection in further stages:
❖ This involves converting the RBG image into greyscale image
❖ Apply gaussian blur
❖ Apply certain threshold value to the image, so that noise can be removed
❖ Apply morphological image processing, dilation and erosion to get neat border of the objects in the image

● Next step is to draw contours around the area, that has been changed in the two images.
● OpenCV allows to detect the presence of contours using inbuilt functions, we can highlight the area that has changed by drawing a
rectangle around it. This area must be greater than a certain threshold value (used as 5000 pixels in our project).

● Once the above rectangle is drawn, we know that certain amount of area (number of pixels) has been changed in the consecutive images. 
Thus, the next step is to go for human detection.

For human detection:
● For detecting the presence of human in the frame, we have used the haar cascades classifiers present in opencv. It is a machine 
learning based approach where a cascade function is trained from a lot of positive and negative images.

● There are different xml files present in opencv which are pre trained to detect humans based on different parts e.g., the upper part,
the lower part, face,eyes etc. All we have to do is include the respective xml in our code and extract the related features from the
image.

The in-depth implementation of Haar classifiers can be found from the OpenCV documentation page:
https://docs.opencv.org/3.3.0/d7/d8b/tutorial_py_face_detection.html

● only the face detection is used as using other classifiers was creating some lag in the raspberry pi. For this to work perfectly, 
the face of human and shoulders must be towards the camera. The side pose did not give accurate results for us.

● Thus, if a face is detected, we have triggered the recording for a certain amount of time. Once recording finishes the loop starts 
again. Taking the current frame as previous frame and taking fresh frame using Picamera.


