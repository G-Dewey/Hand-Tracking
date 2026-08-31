class Hand:
    def __init__(self, landmarks, handedness):
        self.landmarks = landmarks
        self.handedness = handedness
        self.is_open = self._detect_is_open()

    def detect_is_open(self):
        """Returns True if 3 or more fingers are extended above their knuckles."""
        tip_ids = [8, 12, 16, 20]
        pip_ids = [6, 10, 14, 18]

        extended_count = sum(
            1 for tip, pip in zip(tip_ids, pip_ids)
            if self.landmarks[tip].y < self.landmarks[pip].y
        )

        return extended_count >= 3