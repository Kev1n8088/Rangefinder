Day to Day Log

Jun 19 2021: 

Wrote up general design and formulas for the rangefinder. Ordered parts, except the beams and mounting hardware.

Jun 26:  

Parts arrived, refamiliarized myself with servo hardware. Will have to do servo calibration, but that's a job for later. Cameras appear to be in working order.

Jul 3:  

Pt1. For some reason cameras seem to only display the 3:4 aspect ratin instead of the 9:16 that it’s supposed to display in python. 

Pt2. It appears that Imutils, a shortcut library for openCV, only supports video streams in the 3:4 aspect ratio. Luckily, I can simply use openCV’s stock video stream function (with a bit of formatting) to get the original 9:16 video stream.

Jul 10:  

Single camera color marking appears to be in working order, and appears to mark the correct. Added a second camera to the script, also appears to be in working order

Jul 17:  

Worked on serial link between arduino and computer. As expected (based on previous experience with the Kerbal Controller), the arduino quickly desynced and got messy. I did some experimentation and found that a 250ms delay between messages made for a relatively fast update speed while ensuring the arduino stayed synced up. 

Jul 24:  

Looked into stereo vision. Appears to require focal length, as I don’t have that, I am going to attempt to try and make some janky software that assumes that the pixel measurements are completely in proportion with the angle to the camera. Probably won’t be accurate, but it could be a good start.

Aug 1:  

Finished pixel measurement-camera angle software, while it is partially working, moving the object side to side messes up with distance calculations immensely. Unacceptable results, must modify. 

Aug 8:  

Realized that I do have focal length data, went to workshop for some assistance with stereo vision theory. While there, I also assembled the three modules (Main controller + turret, and the two side camera modules). 

Aug 9:  

Cut the rest of the aluminum rods to half-length. Now, the camera modules will be 400mm away from the main module instead of 800mm. Attached all modules to each other with the newly cut aluminum rods. 

Aug 10:  

Finished new, proper stereo vision software. While the results are more promising, the distance still changes when the object is shifted left to right. Did some research, results are likely due to camera distortion. Will need to correct in software. 

Aug 11:  

Finished distortion correction software, testing shows the images modified. Unfortunately the 150 degree cameras will now be limited to 85 degrees due to the distortion correction cutting off a majority of the image.

Aug 12:  

Incorporated distortion correction software, distance is accurate! A truely glorious moment. However, there is a large blind zone in front of the turret due to the limited viewing angle. Will need to accommodate angling of cameras in software.

Aug 13:  

Added camera angling, now the blind zone is mostly countered. Working on turret director software. 

Aug 14:  

Pt1. Finished turret director software, testing is very promising. Tweaked targeting location, and added additional variables for easy correction of any slight errors in the targeting.

Pt2. Created and edited video demonstration. The project is finished. 
