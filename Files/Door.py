import cv2
import face_recognition
import os
from pathlib import Path
import pickle
from collections import Counter
import serial
import time
from datetime import datetime
from encoder import encode_known_faces
from encoder import _recognize_face
from encoder import DEFAULT_ENCODINGS_PATH

# Constant to define a specific time for after hours
AFTER_HOURS = datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)  # 4:00 PM

# Initialize serial communication with arduino
ser = serial.Serial('COM5', 9600)  # Check Device manager for COM number

# Function to send message to arduino just to make things look simpler
def send_to_arduino(message):
    ser.write(message.encode())


# Main function
def main():

    ##################################################################################
    # encode_known_faces()    # IF HAVEN'T CREATED AN ENOCODING FILE, RUN THIS LINE ONCE
    ##################################################################################


    # Load known faces and names from encodings file
    with open(DEFAULT_ENCODINGS_PATH, "rb") as f:
        loaded_encodings = pickle.load(f)

    # Open webcam
    video_capture = cv2.VideoCapture(0)

    log = []  # List to store log messages
    

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        
        message_sent = False    # Flag to make sure only ONE message is sent to arduino and only ONE log is generated 

        
        # Check if 's' key is pressed to start face detection
        if cv2.waitKey(1) & 0xFF == ord('s'):
            print("Scanning...\n")
            # send_to_arduino("Face Detection Mode")
            start_time = time.time()    # timer for 3 seconds

            while time.time() - start_time < 3:  # 3 seconds for face detection
                
                # frame = video_capture.read()

                # Find faces in the frame
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                # Loop through each face found in the frame
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    # Recognize face using loaded encodings
                    name = _recognize_face(face_encoding, loaded_encodings)
                    if name:
                        # Send message to Arduino
                        message = "Known Face OK" if datetime.now() < AFTER_HOURS else "Known Face AFTER HOURS"
                        logmsg = f"Known Face: {name} OK" if datetime.now() < AFTER_HOURS else f"Known Face: {name} AFTER HOURS"
                        # Ensure only ONE message is sent
                        if message_sent == False:
                            print(message + "\n")
                            send_to_arduino(message)
                            log.append((datetime.now(), logmsg))
                            # Set flag to show that a message was sent and a log was generated
                            message_sent = True
                    else:
                        # Send message to Arduino
                        message = "Unknown Face OK" if datetime.now() < AFTER_HOURS else "Unknown Face AFTER HOURS"
                        # Ensure only ONE message is sent
                        if not message_sent:
                            print(message + "\n")
                            send_to_arduino(message)
                            log.append((datetime.now(), message))
                            # Set flag to show that a message was sent and a log was generated
                            message_sent = True

                # print("msg sent\n")

                # Break the loop when 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("quit\n")
                    break
                
            

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Save logs to a text file
    with open(f"{datetime.now().strftime('%Y-%m-%d')} logs.txt", "w") as f:
        for timestamp, message in log:
            f.write(f"{timestamp}: {message}\n")

    # Release the webcam and close the OpenCV window
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()