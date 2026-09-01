import config
from debug import debug
from gamestate import gamestate
import hand

import cv2
import mediapipe as mp
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

        # Initialize MediaPipe Hands
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=config.MAX_HANDS,
            min_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.draw = mp.solutions.drawing_utils

        self.w = 0
        self.h = 0

    def __del__(self):
        # Release the webcam resource when the object is destroyed
        self.cap.release()
        cv2.destroyAllWindows()
        debug.log("Camera resource released.")

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

    def stream(self):
        ret, frame = self.cap.read()
        if not ret:
            debug.log("Failed to read frame from camera.")

        frame, hands = self.process_frame(frame)
        cv2.imshow('Camera Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            debug.log("Exiting camera stream.")
            cv2.destroyAllWindows()
            gamestate.running = False

        return hands

    def process_frame(self, frame):
        frame = cv2.flip(frame, 1)
        self.h, self.w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        hands = []

        if results.multi_hand_landmarks:
            # draw hand landmarks and create Hand objects
            for index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[index]
                hand_obj = hand.Hand(hand_landmarks, handedness, self.w, self.h)

                if self.check_in_border(hand_obj):
                    hand_obj.set_in_border()
                    hands.append(hand_obj)

                self.draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

        if len(hands) > 0:
            border_color = (0, 255, 0)  # Green
        else:
            border_color = (0, 0, 255)  # Red

        # Draw border and text
        cv2.rectangle(frame, (config.BORDER_PADDING, config.BORDER_PADDING), (self.w - config.BORDER_PADDING, self.h - config.BORDER_PADDING), border_color, 2)

        return frame, hands

    def check_in_border(self, hand):
        if (hand.x < config.BORDER_PADDING or hand.x > self.w - config.BORDER_PADDING):
            return False
        if (hand.y < config.BORDER_PADDING or hand.y > self.h - config.BORDER_PADDING):
            return False
        return True

    # Used to get dimensions of the playzone for the game window
    def get_playzone(self):
        return (self.w - (2 *config.BORDER_PADDING)) * config.SCALE_FACTOR, (self.h - ( 2* config.BORDER_PADDING)) * config.SCALE_FACTOR