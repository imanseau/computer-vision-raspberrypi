# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
 
 # initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
  
# allow the camera to warmup
time.sleep(0.1)
   
# Set Flags and values for image processesing 
scale = True
scale_percent = 50 # Scale Percentage
rotate = True
rotate_degrees = 90 # Clockwise rotation (90, 180, 270)
flip_ver = False
flip_hor = False
display_video = True

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    if rotate: # If True rotate by rotate_degrees
        if rotate_degrees == 90:
            image = cv.rotate(image, cv.ROTATE_90_CLOCKWISE)
        if rotate_degrees == 180:
            image = cv.rotate(image, cv.ROTATE_180_CLOCKWISE)
        if rotate_degrees == 270:
            image = cv.rotate(image, cv.ROTATE_270_CLOCKWISE)

    # If True flip
    if flip_ver: image = cv.flip(image, 0)
    if flip_hor: image = cv.flip(image, 1)

    if scale: # If True scale the image
        # calculate the new dimensions
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dsize = (width, height)
        # resize image
        image = cv.resize(image, dsize)

    # show the frame
    cv.imshow("Frame", image)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    key = cv.waitKey(1)
    if key in [27, ord('q')]:
        break
