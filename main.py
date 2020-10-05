import pygame
import json
import random
import time

# from numpy import arange
from gamepad import NotNotController

# Define some colors.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (77,) * 3

class GameDrawer():

    def __init__(self, width, height, caption, font_name=None, font_size=60):
        self.width = width
        self.height = height
        self.caption = caption

        pygame.init()
        self._font = pygame.font.SysFont(font_name, font_size)
        self._bgcolor = BLUE
        self.screen = pygame.display.set_mode((width, height))

        self._timer_bounds = pygame.Rect((self.width - 400) // 2, (self.height - 400) // 2, 400, 400)
        pygame.display.set_caption(caption)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, name_size):
        name, size = name_size
        self._font = pygame.font.SysFont(name, size)

    @property
    def bgcolor(self):
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, color):
        self._bgcolor = color

    def refresh(self):
        pygame.display.flip()

    def fill_screen(self):
        self.screen.fill(self._bgcolor)

    def display_ball(self, position=None, color=WHITE, radius=5):
        if position is None:
            position = (self.width // 2, self.height // 2)
        self.ball_pos = position

        pygame.draw.circle(self.screen, color, position, radius)

    def display_timer(self, angle, color=WHITE, width=5):
        pygame.draw.arc(self.screen, color, self._timer_bounds, 0, angle, width)

    def display_text(self, text, color=BLACK):
        self.screen.fill(self._bgcolor)

        text = self.font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.center = (self.width // 2, self.height // 2)
        self.screen.blit(text, text_rect)




if __name__ == '__main__':
    drawer = GameDrawer(500, 500, 'Test')

    running = False
    continued = False

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Gamepad settings
    with open('logitechF310-mappings.json', 'rt') as f:
        gamepad_settings = json.load(f)

    logitech_gamepad = NotNotController(pygame.joystick.Joystick(0), gamepad_settings)

    ####################################################################
    #                        Starting Countdown                        #
    ####################################################################
    for count_down in range(3, 0, -1):
        for angle in (x / 10 for x in range(63, -1, -1)):
            drawer.fill_screen()

            # text = font.render(f'STARTING IN {count_down}', True, GREY)
            # text_rect = text.get_rect()
            # text_rect.center = (WIDTH // 2, HEIGHT // 2)
            # screen.blit
            drawer.display_text(f'STARTING IN {count_down}', GREY)

            # pygame.draw.arc(screen, WHITE, timer_border, 0, angle, 5)
            # pygame.display.flip()
            drawer.display_timer(angle)

            drawer.refresh()

            clock.tick(60)
    ###################################################################

