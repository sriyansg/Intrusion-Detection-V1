This project implements a simple motion detection alarm system using Python and OpenCV. The system captures live video feed from a webcam, detects motion by analyzing frame differences, and triggers an audible alarm when significant movement is detected.

**Features**

Real-Time Motion Detection: The system continuously monitors video feed for any motion by comparing each frame to a baseline.
Audible Alarm: When motion is detected, an alarm sound is triggered to alert the user.
User-Controlled Alarm Mode: The motion detection and alarm system can be toggled on and off by the user.
Adjustable Parameters: The system uses adjustable parameters for frame processing, such as resizing, grayscaling, and Gaussian blur, to optimize motion detection accuracy.

**How It Works** 

Initial Setup: The program initializes the webcam, captures an initial frame, and processes it to create a baseline image.
Frame Analysis: Each subsequent frame is compared to the baseline image. If a significant change is detected (indicating motion), the system increases an alarm counter.
Alarm Trigger: If the alarm counter exceeds a threshold, an alarm sound is triggered, indicating potential movement in the monitored area.
User Interaction: The user can toggle the motion detection mode on and off by pressing 't'. The program can be exited by pressing 'q'.

**Requirements**

Python 3.x
OpenCV
imutils
winsound (available on Windows)
