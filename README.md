# Face-Detection-Door-Security-Project
This is a Face Detection Secure Access Point System

[Face Encoding](https://github.com/ishwo0/Face-Detection-Door-Security-Project/tree/main/Files/output)

[Training Data](https://github.com/ishwo0/Face-Detection-Door-Security-Project/tree/main/Files/training/jack_black)

[Main Execution File](https://github.com/ishwo0/Face-Detection-Door-Security-Project/tree/main/Files/output)

## The Project

This system is a design for a secure access point for applications such as employee-only doors. The system includes a PC to run a [Python File](https://github.com/ishwo0/Face-Detection-Door-Security-Project/blob/main/Files/Door.py) that handles the webcam and face detection function, an Arduino to handle event decoding and hardware behavior, and an LCD screen to mimic a door. The PC will communicate with the Arduino through UART by USB. Upon receiving messages, the Arduino will interpret each message and trigger the appropriate behavior for the LCD screen. Furthermore, there will be logs generated upon termination of the Python program (shutdown).

- [output folder](https://github.com/ishwo0/Face-Detection-Door-Security-Project/tree/main/Files/output)
  - This folder contains the encoding file for each face in the training folder database
- [training folder](https://github.com/ishwo0/Face-Detection-Door-Security-Project/tree/main/Files/training)
  - This folder contains all of the training data (images of faces) that will be used to decide who gets access
- [Door.py](https://github.com/ishwo0/Face-Detection-Door-Security-Project/blob/main/Files/Door.py)
  - This file is the main Python file that will run in the system
- [encoder.py](https://github.com/ishwo0/Face-Detection-Door-Security-Project/blob/main/Files/encoder.py)
  - This file is a Python file containing the encoding and face_recognition functions used in Door.py
