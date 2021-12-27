from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

vs1 = cv2.VideoCapture(2)
vs1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vs1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    r, frame = vs1.read()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            break
