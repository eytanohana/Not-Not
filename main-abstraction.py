import pygame
import json
import random
import time

from gamepad import NotNotController
from direction import Direction
from main import GameDrawer

BLACK = (0,) * 3
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255,) * 3
GREY = (77,) * 3
GREEN = (11, 212, 51)
ORANGE = (230, 163, 48)

speed = 0.015
ball_speed = 14


def play_game(difficulty):
    lives = 3
    directions = Direction(difficulty=difficulty)

    ####################################################################
    #                        Starting Countdown                        #
    ####################################################################
    for count_down in range(3, 0, -1):
        # in radians 2pi, pi, 0
        for angle in (a / 10 for a in range(63, -1, -1)):
            if count_down == 2:
                angle = -angle
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
    lost = False
    # Each game is 20 rounds long.
    turn = 10
    while turn > 0:
        time.sleep(0.1)
        if lost:
            if lives > 0:
                drawer.display_option('use a life and continue?')
                drawer.display_lives(lives)
                drawer.refresh()
                while (input_direction := gamepad.direction_input()) is None:
                    pygame.event.get()

                if input_direction == 'LEFT':
                    lives -= 1
                    lost = False
                    time.sleep(0.5)

                else:
                    print('round lost')
                    return False

            else:
                drawer.bgcolor = ORANGE
                drawer.display_lose()
                time.sleep(1)
                return False

        # User did something.
        for event in pygame.event.get():
            # If user clicked close.
            if event.type == pygame.QUIT:
                pass

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

            drawer.display_text(f'{turn}', position=(drawer.width - 50, 50))

            # draw the ball in the proper place
            drawer.display_ball(ball_pos)
            drawer.display_lives(lives)
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
                if directions.correct_direction(input_direction):
                    # Leave the for; go on to the next turn.
                    turn -= 1
                    break

                # The player chose wrong.
                else:
                    drawer.bgcolor = RED
                    drawer.fill_screen()

                    drawer.display_text("You chose wrong!")
                    drawer.display_lives(lives)
                    drawer.refresh()
                    time.sleep(0.3)
                    # prompt to use a life and play again above
                    lost = True
                    break

        # The ball didn't reach the end.
        # The player was too slow and time ran out.
        else:

            drawer.bgcolor = RED
            drawer.fill_screen()
            drawer.display_text('Out of Time! You were too slow.')
            drawer.display_lives(lives)
            drawer.refresh()
            time.sleep(1)
            if lives > 0:
                drawer.display_option('use a life and continue?')
                drawer.display_lives(lives)
                drawer.refresh()

                while (input_direction := gamepad.direction_input()) is None:
                    pygame.event.get()

                time.sleep(0.5)

                if input_direction == 'LEFT':
                    lives -= 1
                    time.sleep(1)

            else:
                drawer.bgcolor = ORANGE
                drawer.display_lose()
                time.sleep(1)
                return False


    # The player completed the round successfully.
    else:
        drawer.bgcolor = GREEN
        drawer.fill_screen()
        drawer.display_text('Congratulations', WHITE)
        drawer.refresh()
        time.sleep(2)
        return True

    drawer.refresh()
    # Limit to 20 frames per second.
    clock.tick(20)



if __name__ == '__main__':
    drawer = GameDrawer(800, 500, 'NOT NOT')
    icon = pygame.image.load('exclamation-mark.png')
    pygame.display.set_icon(icon)

    # Set up the direction object


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

    print(play_game(2))