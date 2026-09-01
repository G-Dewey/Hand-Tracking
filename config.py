# DEBUG SETTINGS
DEBUG_LOG = False
DEBUG_CONSOLE = True

# CAMERA SETTINGS
CAMERA_INDEX = 1  # Default camera index (0 for the first camera)
MAX_HANDS = 2  # Maximum number of hands to detect
MIN_DETECTION_CONFIDENCE = 0.5  # Minimum confidence for hand detection
MIN_TRACKING_CONFIDENCE = 0.5  # Minimum confidence for hand tracking
BORDER_PADDING = 100  # Padding for the border around the frame

# GAME SETTINGS
SCALE_FACTOR = 2.0  # Scale factor for resizing the game window (1.0 = original size, 0.5 = half size, etc.)
BACKGROUND_COLOR = (200, 200, 200)  # Background color of the game window (RGB format)

# OUTPUT SETTINGS
LOGS_FOLDER_PATH = "output/logs"
CAPTURES_FOLDER_PATH = "output/caps"