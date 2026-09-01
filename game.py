import config
from debug import debug

import pygame

class Game:
    def __init__(self,w,h):
        # Initialise the game
        pygame.init()
        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("hand tracking demo")
        self.clock = pygame.time.Clock()

    def frame(self, hands):
        # Fill the screen with a color (e.g., black)
        self.screen.fill(config.BACKGROUND_COLOR)

        # Hands
        hand_objects = [Hand(hand.is_open, hand.handedness, hand.in_border_x, hand.in_border_y) for hand in hands]

        for obj in hand_objects:
            obj.draw(self.screen)

        # Update the display
        pygame.display.flip()

        # Limit the frame rate
        self.clock.tick(60)

class Hand:
    def __init__(self, open, handedness, x, y):
        self.open = open
        self.handedness = handedness.classification[0].label.lower()  # Get the label (e.g., "left" or "right")
        self.x = x*config.SCALE_FACTOR
        self.y = y*config.SCALE_FACTOR 
        self.image = pygame.image.load("assets/hand/open.png" if self.open else "assets/hand/closed.png")
        if self.handedness == "right":
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (32, 64))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)