import pygame
import json
import random
import time

# from numpy import arange
from gamepad import NotNotController

# Define some colors.
BLACK = (0,) * 3
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255,) * 3
GREY = (77,) * 3

directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
speed = 0.015

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

    def display_text(self, text, color=BLACK, position=None):
        text = self.font.render(text, True, color)
        text_rect = text.get_rect()
        if position is None:
            position = self.width // 2, self.height // 2
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def ball_in_border(self):
        return (self.ball_pos[0] > self._timer_bounds.left and self.ball_pos[0] < self._timer_bounds.right
            and self.ball_pos[1] > self._timer_bounds.top and self.ball_pos[1] < self._timer_bounds.bottom)


def float_range(start, stop, step=1):
    """
    Helper function since normal python range
    doesn't support floats.
    """
    i = start
    if start <= stop:
        while i <= stop:
            yield i
            i += step
    else:
        while i >= stop:
            yield i
            i += step


if __name__ == '__main__':
    # Set up the drawer object
    drawer = GameDrawer(800, 500, 'NOT NOT')

    # flags
    running = True

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Gamepad settings
    with open('logitechF310-mappings.json', 'rt') as f:
        gamepad_settings = json.load(f)

    gamepad = NotNotController(pygame.joystick.Joystick(0), gamepad_settings)

    ####################################################################
    #                        Starting Countdown                        #
    ####################################################################
    for count_down in range(3, 0, -1):
        for angle in float_range(6.3, 0, -1):
            # Color the screen
            drawer.fill_screen()
            # Draw the countdown
            drawer.display_text(f'STARTING IN {count_down}', GREY)
            # Draw the circular timer
            drawer.display_timer(angle)
            # Flip
            drawer.refresh()
            # 60 fps
            clock.tick(60)
    ###################################################################

    # ---------- Main Program Loop ------------
    while running:
        time.sleep(0.1)

        # User did something.
        for event in pygame.event.get():
            # If user clicked close.
            if event.type == pygame.QUIT:
                running = False

        # Choose a random direction either up right left or down
        target_direction = random.choice(directions)

        prev_input_direction = None

        for angle in float_range(6.3, 0, -1):

            # display the information
            drawer.fill_screen()
            drawer.display_text(target_direction, GREY)

            # draw the ball in the proper place
            drawer.display_ball()

            # makes it easier to get controller input
            pygame.event.get()
            # capture the controller input
            input_direction = gamepad.direction_input()

            # Initialize the previous input
            # We need prev_input_direction otherwise
            # input_direction is None most of the time.
            # prev_ lets the ball continue to update after
            # choosing a direction.
            #
            # Need to update later to be able to correct a wrong move in time.
            # But for now it works good enough.
            if prev_input_direction is None:
                prev_input_direction = input_direction
            else:
                input_direction = prev_input_direction

            # get the input
            if input_direction is not None:
                # update the balls position
                if input_direction == 'LEFT':
                    drawer.ball_pos[0] -= 10

                elif input_direction == 'RIGHT':
                    drawer.ball_pos[0] += 10

                elif input_direction == 'UP':
                    drawer.ball_pos[1] -= 10

                else:
                    drawer.ball_pos[1] += 10
                #####################################

            # If the ball reached the end.
            if not drawer.ball_in_border():

                # The player chose correct.
                if input_direction == target_direction:
                    print('SUCCESS')
                    # Leave the for; go on to the next turn.
                    break

                # The player chose wrong.
                else:
                    print('FAIL')
                    drawer.bgcolor = RED
                    drawer.fill_screen()

                    drawer.display_text("You chose wrong!")
                    drawer.refresh()
                    time.sleep(0.3)
                    # end the game
                    running = False
                    break

            # The ball didn't reach the end.
            # The player was too slow.
            else:
                if angle == 0:
                    print('FAIL')
                    drawer.bgcolor = RED
                    drawer.fill_screen()

                    drawer.display_text('Out of Time! You were too slow.')
                    # pygame.display.flip(
                    drawer.refresh()
                    time.sleep(3)
                    done = True
                    break
            ###########################################
            # pygame.draw.arc(screen, WHITE, timer_border, 0, angle, 5)
            drawer.display_timer(angle)

            # pygame.display.flip()
            drawer.refresh()
            time.sleep(speed)
        ####################################################################

        #
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        #

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second.
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
