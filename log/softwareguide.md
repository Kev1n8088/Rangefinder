**Software Guide**

**Computer:**

I first used OpenCV to find the largest circles of our designated color in our two camera feeds. The X and Y data of this circle is fed to our locator function, which uses the data of the two cameras, the focal length of the cameras, the sensor size of the cameras, the distance between the cameras, and the angle of the cameras to determine the X, Y, and Z location of the object. I first determine the X and Y angle of the object in our two cameras, using inverse tan. To find Z, I find the distance the object is from our two cameras by using tan. After I find the two distances, I can then use Heron’s Formula to find the area of the triangle, and then divide that by half of the distance between the two cameras. To find X, I simply use the Pythagorean formula as I already know two of the sides (the distance to the camera, and Z, both calculated previously). And finally, to find Y, I use the distance the object is from our cameras, and then use sin and the Y angle to find the Y coordinate. I then feed these three coordinates into another function, which uses inverse tan to find the angle in which the turret should be pointing in order to hit the target, and incorporates bullet drop into the final result for a more accurate shot. This data is sent via serial port to our arduino, which receives it and guides the turret appropriately.

**Arduino:** 

I take the data from our serial port, and first split it into the X and Y angles. I then take that data and feed it into our servos, which turn to the correct angle to point our turret at the target. Really, this part of the code is very simple, basically just pulling data from the serial stream and directing the servo based on that data
