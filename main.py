import config
import game
from gamestate import gamestate
from debug import debug
from cam import Camera

cam = Camera(camera_index=config.CAMERA_INDEX)
cam.stream()
w,h = cam.get_playzone()
game = game.Game(w, h)

# MAIN LOOP
while gamestate.running:
    hands = cam.stream()
    game.frame(hands)

del cam