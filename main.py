import config
from debug import debug
from cam import Camera

cam = Camera(camera_index=config.CAMERA_INDEX)
cam.start_stream()

del cam