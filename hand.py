import config
from debug import debug


class Hand:
    def __init__(self, landmarks, handedness, frame_w, frame_h):
        self.landmarks = landmarks
        self.handedness = handedness
        self.is_open = self.detect_is_open()
        self.x, self.y = self.get_palm_center(frame_w, frame_h)
        self.in_border_x = 0
        self.in_border_y = 0

    def detect_is_open(self):
        """Returns True if 3 or more fingers are extended above their knuckles."""
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]

        extended_count = sum(
            1 for tip, pip in zip(tip_ids, pip_ids)
            if self.landmarks.landmark[tip].y < self.landmarks.landmark[pip].y
        )

        return extended_count >= 3

    def get_palm_center(self, frame_w, frame_h):
        palm_ids = [0, 5, 9, 13, 17]
        xs = [self.landmarks.landmark[i].x * frame_w for i in palm_ids]
        ys = [self.landmarks.landmark[i].y * frame_h for i in palm_ids]

        cx = sum(xs) / len(xs)
        cy = sum(ys) / len(ys)

        return int(cx), int(cy)

    def set_in_border(self):
        self.in_border_x = (self.x - config.BORDER_PADDING)
        self.in_border_y = (self.y - config.BORDER_PADDING)