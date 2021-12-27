**Abstract:**

The goal is to create a stereo camera system that can find an object's location in space, calculate the necessary elevation and azimuth for a turret, and direct an arduino turret to aim at the turret. The system should be fairly accurate (Hits a 10x10 cm area at 3 meters), and should be real time (or as close as possible to real time).

I will be using the Python openCV library for object identification, paired with 2 1080p 150 degree wide-angle cameras. I will be using a proprietary formula to determine the location of the 3D space, which I will describe further below. The turret will first be a simple laser, however if I have the time for the testing, I may refit that for a water gun to test projectile drop calculations. 
