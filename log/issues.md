**Issues**

**Hardware: **

X axis servo burned out due to… something? Maybe it just was DOA. Solution: Bought a new one

USB unable to power both servos effectively. Solution: Got a 5 amp Li-Ion battery to power the servos

**Software:**

Imutils defaulted to 3:4 aspect ratio, cutting out a lot of our wide angle features. Solution: Used OpenCV stock video stream function, with a bit of formatting

Cameras were getting fish-eye effects at the edges. Solution: Calibrating the cameras (However this did reduce our FOV significantly)

Our first standard stereo vision method only works if cameras aren’t angled, and without angling cameras I have a massive blind zone right in front of the turret. Solution: Use the Heron’s formula method instead of the standard method

Arduino unable to keep up with max speed serial port datastream. Solution: Cap update frequency to 4 hertz

Turret is slightly off due to inaccuracies in construction or differences in location. Solution: Add variables to account for these, with offsets for both distance and angle.
