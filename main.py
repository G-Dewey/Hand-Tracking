import config
from state import gamestate
from debug import debug
from cam import Camera

cam = Camera(camera_index=config.CAMERA_INDEX)
cam.stream()

# MAIN LOOP
while gamestate.running:
    hands = cam.stream()
    

del cam