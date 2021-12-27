from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

DIM=(1920, 1080)
K=np.array([[1087.7517088403981, 0.0, 921.1974163971402], [0.0, 1100.0717302685962, 543.3721306287408], [0.0, 0.0, 1.0]])
D=np.array([[0.0474937696880302], [-1.2257225826964717], [2.856438084251032], [-2.0954783152258365]])

vs1 = cv2.VideoCapture(1)
vs1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vs1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    r1, frame1 = vs1.read()
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    frame1 = cv2.remap(frame1, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("Frame1", frame1)
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            break
