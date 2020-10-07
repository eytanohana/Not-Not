import pygame
import json
import random
import time

from gamepad import NotNotController
from direction import Direction

# Define some colors.
BLACK = (0,) * 3
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255,) * 3
GREY = (77,) * 3
GREEN = (11, 212, 51)

# directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
speed = 0.015
ball_speed = 13

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

    def display_ball(self, position, color=WHITE, radius=5):
        pygame.draw.circle(self.screen, color, position, radius)

    def display_timer(self, angle, color=WHITE, width=5):
        pygame.draw.arc(self.screen, color, self._timer_bounds, 0, angle, width)

    def display_text(self, text, color=BLACK, position=None):
        text = self.font.render(text, True, color)
        text_rect = text.get_rect()
        if position is None:
            position = [self.width // 2, self.height // 2]
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def display_try_again(self):
        self.fill_screen()
        self.display_text('Play Again?')
        self.display_text('<- ok       no thanks->', position=(self.width // 2, self.height // 2 + 50))
        self.refresh()

    def ball_in_border(self, ball_pos):
        return (self._timer_bounds.left < ball_pos[0] < self._timer_bounds.right
                and self._timer_bounds.top < ball_pos[1] < self._timer_bounds.bottom)




if __name__ == '__main__':
    print('Icons made by <a href="https://www.flaticon.com/authors/pixel-buddha" title="Pixel Buddha">Pixel Buddha</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>')
    # Set up the drawer object
    drawer = GameDrawer(800, 500, 'NOT NOT')
    icon = pygame.image.load('exclamation-mark.png')
    pygame.display.set_icon(icon)

    # Set up the direction object
    directions = Direction(difficulty=2)

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
        # in radians 2pi, pi, 0
        for angle in (a / 10 for a in range(63, -1, -1)):
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

        lost = False
        # Each game is 20 rounds long.
        for round in range(10, 0, -1):
            time.sleep(0.1)
            if lost:
                drawer.display_try_again()

                input_direction = None
                while (input_direction := gamepad.direction_input()) is None:
                    pygame.event.get()

                if input_direction == 'LEFT':
                    print('CONTINUING')
                else:
                    running = False

                time.sleep(1)
                break

            # User did something.
            for event in pygame.event.get():
                # If user clicked close.
                if event.type == pygame.QUIT:
                    running = False

            # Choose a random direction either up right left or down
            # target_direction = random.choice(directions)
            directions.pick_direction()

            prev_input_direction = None
            ball_pos = [drawer.width // 2, drawer.height // 2]

            drawer.bgcolor = BLUE

            for angle in (a / 10 for a in range(63, -1, -1)):
                time.sleep(speed)

                # display the information
                drawer.fill_screen()
                drawer.display_text(directions.target_direction, GREY)

                drawer.display_text(f'{round}', position=(drawer.width - 50, 50))


                # draw the ball in the proper place
                drawer.display_ball(ball_pos)

                drawer.display_timer(angle)
                drawer.refresh()

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
                        ball_pos[0] -= ball_speed

                    elif input_direction == 'RIGHT':
                        ball_pos[0] += ball_speed

                    elif input_direction == 'UP':
                        ball_pos[1] -= ball_speed

                    else:
                        ball_pos[1] += ball_speed

                # If the ball reached the end.
                if not drawer.ball_in_border(ball_pos):

                    # The player chose correct.
                    # if input_direction == target_direction:
                    if directions.correct_direction(input_direction):
                        # Leave the for; go on to the next turn.
                        break

                    # The player chose wrong.
                    else:
                        drawer.bgcolor = RED
                        drawer.fill_screen()

                        drawer.display_text("You chose wrong!")
                        drawer.refresh()
                        time.sleep(0.3)
                        # end the game
                        lost = True
                        break

            # The ball didn't reach the end.
            # The player was too slow.
            else:

                drawer.bgcolor = RED
                drawer.fill_screen()

                drawer.display_text('Out of Time! You were too slow.')
                drawer.refresh()

                time.sleep(1)
                # play again
                # drawer.fill_screen()
                # drawer.display_text('Play Again?')
                # drawer.display_text('<- ok       no thanks->', position=(drawer.width//2 , drawer.height//2+50))
                # drawer.refresh()
                # time.sleep(1)
                drawer.display_try_again()

                while (input_direction := gamepad.direction_input()) is None:
                    pygame.event.get()

                if input_direction == 'LEFT':
                    print('CONTINUING')
                    time.sleep(1)
                    break

                running = False
                break

        # The player completed the round successfully.
        else:
            drawer.bgcolor = GREEN
            drawer.fill_screen()
            drawer.display_text('Congratulations', WHITE)
            drawer.refresh()
            time.sleep(2)
            running = False



        drawer.refresh()
             # Limit to 20 frames per second.
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
