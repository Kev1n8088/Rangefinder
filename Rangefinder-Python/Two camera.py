# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import serial
#distance between two cameras (millimeters)
difX = 1100

#camera specs
f = 2.1
sensorW = 3.55
sensorH = 2.67
t1multi = 2
#offset inward from perpendicular
angleOffsetX = 30
#offset upward from perpendicular
angleOffsetY = 0

#offset of the turret in distance, for fine adjustments
#upward
turretOffsetY = 120
#right
turretOffsetX = -100
#forward
turretOffsetZ = 0

#offset of the turret in angles, for fine adjustments
#upward
turretOffsetAngleY = 2
#right
turretOffsetAngleX = 0

#millimeters per second
muzzleVelocity = 299792458000
gravity = 9810

#correction specs
DIM=(1920, 1080)
K=np.array([[1087.7517088403981, 0.0, 921.1974163971402], [0.0, 1100.0717302685962, 543.3721306287408], [0.0, 0.0, 1.0]])
D=np.array([[0.0474937696880302], [-1.2257225826964717], [2.856438084251032], [-2.0954783152258365]])

# construct the argument parsse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-b", "--buffer", type=int, default=64,
        help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (88, 106, 47)
greenUpper = (151, 255, 173)
pts1 = deque(maxlen=args["buffer"])
pts2 = deque(maxlen=args["buffer"])

#camera 1 = left camera 2 = right
vs1 = cv2.VideoCapture(2)
vs2 = cv2.VideoCapture(0)

#VideoStream(src=1).start()

vs1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vs1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
vs2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vs2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# allow the camera or video file to warm up

width = 1280
height = 720

time.sleep(2.0)
x1, y1 = -1, -1
x2, y2 = -1, -1
x, y = -1, -1
z = -1
zList = []
zAvg = 0

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.25)
    data = arduino.readline()
    return data

def zFocus(x1, x2):
        w1 = width/2
        x1 = (x1 - w1) / w1 * sensorW
        x2 = (x2 - w1) / w1 * -sensorW
        z = -1
        if (x1 - x2) != 0:
                z = ((x1 + x2)/f) / difX
                z = np.reciprocal(z)
        return(z)

def findXYZ(x1, x2, y1, y2):
        #pixel measurement to angles
        ax1 = np.degrees(np.arctan(f/((x1 - (width/2))/width * sensorW)))
        if ax1 < 0:
                ax1 = ax1 + 180 
        ax1 = ax1 - angleOffsetX
        ax2 = np.degrees(np.arctan(f/((-x2 + (width/2))/width * sensorW)))
        if ax2 < 0:
                ax2 = ax2 + 180 
        ax2 = ax2 - angleOffsetX
        ax3 = 180 - ax1 - ax2
        print(ax1, ax2)
        
        if ((-y1 + (height/2))/height * sensorH) != 0:
                ay1 = np.degrees(np.arctan(f/((y1 - (height/2))/height * sensorH))) + angleOffsetY
        else:
                ay1 = np.degrees(np.arctan(f/(((y1 - (height/2))/height * sensorH) + 0.001))) + angleOffsetY
        if ay1 < 0:
                ay1 = (ay1 + 90)
        else:
                ay1 = (ay1 - 90)
        if ((-y2 + (height/2))/height * sensorH) != 0:
                ay2 = np.degrees(np.arctan(f/((y2 - (height/2))/height * sensorH))) + angleOffsetY
        else:
                ay2 = np.degrees(np.arctan(f/(((y2 - (height/2))/height * sensorH) + 0.001))) + angleOffsetY
        if ay2 < 0:
                ay2 = (ay2 + 90)
        else:
                ay2 = (ay2 - 90)

        #find 3 sides with trig
        ratio = np.sin(np.radians(ax3)) / difX
        d1 = np.sin(np.radians(ax2)) / ratio
        d2 = np.sin(np.radians(ax1)) / ratio

        #using herons formula to find area and then height, giving us z
        s = (d1 + d2 + difX) / 2
        area = np.sqrt(s * (s - d1) * (s - d2) * (s - difX))
        z = area * 2 / difX
        z = z - turretOffsetZ

        #use pythagorean formula to find x
        x = ((np.sqrt((d1**2) - (z**2)) - (difX/2)) + (-(np.sqrt((d2**2) - (z**2))) + (difX/2)))/2 + turretOffsetX

        #find y with trig
        #can change diag to just be z, need to test
        diag1 = np.sqrt((abs(x + difX/2) ** 2) + (z ** 2))
        diag2 = np.sqrt((abs(-x + difX/2) ** 2) + (z ** 2))
        y = ((np.sin(np.radians(ay1)) * diag1) + (np.sin(np.radians(ay2)) * diag2))/2 - turretOffsetY
        
        
        return x, y, z

def turretAngle(x, y, z):
        d = np.sqrt((x**2) + (y**2) + (z**2))
        t = d / muzzleVelocity
        drop = (t * gravity) / 2 * t
        y = y + drop
        xAngle = np.degrees(np.arctan(x/z)) + turretOffsetAngleX
        diag = np.sqrt((abs(x) ** 2) + (z**2))
        yAngle = np.degrees(np.arctan(y/diag)) + turretOffsetAngleY
        
        return xAngle, yAngle

# keep looping
while True:
        # grab the current frames
        r1, frame1 = vs1.read()
        r2, frame2 = vs2.read()
        frame1 = frame1[1] if args.get("video", False) else frame1
        if frame1 is None:
                break

        frame2 = frame2[1] if args.get("video", False) else frame2
        if frame2 is None:
                break

        #calibrate frames
        map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
        frame1 = cv2.remap(frame1, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        frame2 = cv2.remap(frame2, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        frame1 = imutils.resize(frame1, width=width)
        frame2 = imutils.resize(frame2, width=width)

        #configuring frames
        blurred1 = cv2.GaussianBlur(frame1, (11, 11), 0)
        hsv1 = cv2.cvtColor(blurred1, cv2.COLOR_BGR2HSV)
        blurred2 = cv2.GaussianBlur(frame2, (11, 11), 0)
        hsv2 = cv2.cvtColor(blurred2, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv1, greenLower, greenUpper)
        mask1 = cv2.erode(mask1, None, iterations=2)
        mask1 = cv2.dilate(mask1, None, iterations=2)
        mask2 = cv2.inRange(hsv2, greenLower, greenUpper)
        mask2 = cv2.erode(mask2, None, iterations=2)
        mask2 = cv2.dilate(mask2, None, iterations=2)

                # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts1 = imutils.grab_contours(cnts1)
        center1 = None
        cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts2 = imutils.grab_contours(cnts2)
        center2 = None
        # only proceed if at least one contour was found
        
        
        if len(cnts1) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c1 = max(cnts1, key=cv2.contourArea)
                ((x1, y1), radius1) = cv2.minEnclosingCircle(c1)
                M1 = cv2.moments(c1)
                center1 = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
                # only proceed if the radius meets a minimum size
                if radius1 > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame1, (int(x1), int(y1)), int(radius1),
                                (0, 255, 0), 2)
                        cv2.circle(frame1, center1, 5, (0, 0, 255), -1)
        print("c1: " + str(int(x1)) + "x" + str(int(y1)))               
        
        
        # update the points queue
        pts1.appendleft(center1)

        if len(cnts2) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c2 = max(cnts2, key=cv2.contourArea)
                ((x2, y2), radius2) = cv2.minEnclosingCircle(c2)
                M2 = cv2.moments(c2)
                center2 = (int(M2["m10"] / M2["m00"]), int(M2["m01"] / M2["m00"]))
                # only proceed if the radius meets a minimum size
                if radius2 > 10:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(frame2, (int(x2), int(y2)), int(radius2),
                                (0, 255, 0), 2)
                        cv2.circle(frame2, center2, 5, (0, 0, 255), -1)
                        
        print("c2: " + str(int(x2)) + "x" + str(int(y2)))
        
        # update the points queue
        pts2.appendleft(center2)

                # loop over the set of tracked points
        for i in range(1, len(pts1)):
                # if either of the tracked points are None, ignore
                # them
                if pts1[i - 1] is None or pts1[i] is None:
                        continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame1, pts1[i - 1], pts1[i], (0, 0, 255), thickness)

        for i in range(1, len(pts2)):
                # if either of the tracked points are None, ignore
                # them
                if pts2[i - 1] is None or pts2[i] is None:
                        continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(frame2, pts2[i - 1], pts2[i], (0, 0, 255), thickness)
        

        
        x, y, z = findXYZ(x1, x2, y1, y2)
        angleX, angleY = turretAngle(x, y, z)

        print(x, y, z)
        print(angleX, angleY)
        write_read(str(int(angleX)) + "x" + str(int(angleY))+ "x")
         
                
        # show the frame to our screen
        cv2.imshow("Frame1", frame1)
        cv2.imshow("Frame2", frame2)
        key = cv2.waitKey(1) & 0xFF
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
                break
        
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
        vs1.stop()
        vs2.stop()
# otherwise, release the camera
else:
        vs1.release()
        vs2.release()
# close all windows
cv2.destroyAllWindows()
