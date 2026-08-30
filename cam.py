import config
from debug import debug

import cv2
from datetime import datetime
from pathlib import Path

class Camera:
    def __init__(self, camera_index=0):
        # Capture folder setup
        self.captures_folder = Path(__file__).parent / config.CAPTURES_FOLDER_PATH
        self.captures_folder.mkdir(exist_ok=True)

        # Establish a connection to the webcam - number refers to the camera index (0 for default camera)
        self.cap = cv2.VideoCapture(camera_index)
        debug.log(f"Camera initialized with index: {camera_index}.")

    def __del__(self):
        # Release the webcam resource when the object is destroyed
        self.cap.release()
        cv2.destroyAllWindows()
        debug.log("Camera resource released.")

    def color_space_conversion(self, frame):
        return frame 

    def capture_frame(self):
        ret, frame = self.cap.read()

        if ret:
            debug.log("Frame captured successfully.")
            frame = self.color_space_conversion(frame)
            filename = self.captures_folder / f"capture_{datetime.now():%Y%m%d_%H%M%S}.jpg"
            if cv2.imwrite(str(filename), frame):
                print(f"Saved frame to {filename}")
            else:
                print("Failed to save the frame.")
        else:
            debug.log("Failed to capture frame.")

    def start_stream(self):
        debug.log("Starting camera stream. Press 'q' to exit.")

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                debug.log("Failed to read frame from camera.")
                break

            frame = self.color_space_conversion(frame)
            cv2.imshow('Camera Stream', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                debug.log("Exiting camera stream.")
                cv2.destroyAllWindows()
                break