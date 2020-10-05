import pygame
import json
import random
import time

import gamepad

WIDTH = 800
HEIGHT = 500

# Define some colors.
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (77,) * 3

RADIUS = 5


directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']
timer_radius = 400
timer_border = pygame.Rect((WIDTH - timer_radius) // 2, (HEIGHT - timer_radius) // 2, timer_radius, timer_radius)

failure_message = 'You Failed :('
success_message = 'Congratulations'

speed = 0.015

def ball_in_border(ball_position):
    return (ball_position[0] > timer_border.left and ball_position[0] < timer_border.right
            and ball_position[1] > timer_border.top and ball_position[1] < timer_border.bottom)


if __name__ == '__main__':
    pygame.init()
    # start the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NOT NOT')

    # Loop until the game ends
    done = False
    continued = False


    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Gamepad settings
    with open('logitechF310-mappings.json', 'rt') as f:
        gamepad_settings = json.load(f)

    logitech_gamepad = gamepad.NotNotController(pygame.joystick.Joystick(0), gamepad_settings)

    font = pygame.font.SysFont(None, 60)

    print(timer_border.left, timer_border.right, timer_border.top, timer_border.bottom)

    ####################################################################
    #                        Starting Countdown                        #
    ####################################################################
    for count_down in range(3, 0, -1):
        for angle in (x / 10 for x in range(63, -1, -1)):
            screen.fill(BLUE)

            text = font.render(f'STARTING IN {count_down}', True, GREY)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)

            pygame.draw.arc(screen, WHITE, timer_border, 0, angle, 5)
            pygame.display.flip()

            clock.tick(60)
    ###################################################################

    # -------- Main Program Loop -----------
    while not done:
        time.sleep(0.1)
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get():  # User did something.
            if event.type == pygame.QUIT:  # If user clicked close.
                done = True  # Flag that we are done so we exit this loop.

        ####################################################################
        #                        Draw the next instruction                 #
        #                                                                  #
        # Pick a random direction, draw the circle in the middle,          #
        #    and listen for user input                                     #
        ####################################################################
        direction = random.choice(directions)

        text = font.render(direction, True, GREY)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)

        ball_position = [WIDTH // 2, HEIGHT // 2]
        prev_input_direction = None

        for angle in (x / 10 for x in range(63, -1, -1)):

            screen.fill(BLUE)
            screen.blit(text, text_rect)
            pygame.draw.circle(screen, WHITE, ball_position, RADIUS)

            pygame.event.get()

            input_direction = logitech_gamepad.direction_input()

            if prev_input_direction is None:
                prev_input_direction = input_direction

            else:
                input_direction = prev_input_direction

            if input_direction is not None:
                # print(input_direction)

                if input_direction == 'LEFT':
                    ball_position[0] -= 10

                elif input_direction == 'RIGHT':
                    ball_position[0] += 10

                elif input_direction == 'UP':
                    ball_position[1] -= 10

                else:
                    ball_position[1] += 10
                #####################################
            if not ball_in_border(ball_position):
                if input_direction == direction:
                    print('SUCCESS')
                    break

                else:
                    print('FAIL')
                    screen.fill(RED)

                    text = font.render(failure_message, True, GREY)
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT // 2)
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    time.sleep(0.3)
                    done = True
                    break
            else:
                if angle == 0:
                    print('FAIL')
                    screen.fill(RED)

                    text = font.render('Time ran out. You were too late.', True, GREY)
                    text_rect = text.get_rect()
                    text_rect.center = (WIDTH // 2, HEIGHT // 2)
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    time.sleep(3)
                    done = True
                    break
            ###########################################
            pygame.draw.arc(screen, WHITE, timer_border, 0, angle, 5)

            pygame.display.flip()
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
