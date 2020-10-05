import pygame
import json
import random
import time

import gamepad



WIDTH = 800
HEIGHT = 500

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (77,) * 3

RADIUS = 5
border = 400

directions = ['LEFT', 'RIGHT', 'UP', 'DOWN']

def handle_direction(direction):
    pygame.event.get()

    if direction == 'LEFT':
        if (logitech_gamepad.is_pressed('X') or logitech_gamepad.left_stick_left()
            or logitech_gamepad.right_stick_left() or logitech_gamepad.dpad_left()):
            print('success')

    elif direction == 'RIGHT':
        if (logitech_gamepad.is_pressed('B') or logitech_gamepad.left_stick_right()
            or logitech_gamepad.right_stick_right() or logitech_gamepad.dpad_right()):
            print('success')


    elif direction == 'UP':
        if (logitech_gamepad.is_pressed('Y') or logitech_gamepad.left_stick_up()
            or logitech_gamepad.right_stick_up() or logitech_gamepad.dpad_up()):
            print('success')

    elif direction == 'DOWN':
        if (logitech_gamepad.is_pressed('A') or logitech_gamepad.left_stick_down()
            or logitech_gamepad.right_stick_down() or logitech_gamepad.dpad_down()):
            print('success')

if __name__ == '__main__':
    pygame.init()
    # start the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NOT NOT')

    # Loop until the game ends
    done = False

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()


    # Gamepad settings
    with open('logitechF310-mappings.json', 'rt') as f:
        gamepad_settings = json.load(f)
        print(gamepad_settings)

    logitech_gamepad = gamepad.Gamepad(pygame.joystick.Joystick(0), gamepad_settings)


    timer_radius = 400
    timer_border = pygame.Rect((WIDTH - timer_radius) // 2, (HEIGHT - timer_radius) // 2, timer_radius, timer_radius)
    font = pygame.font.SysFont(None, 60)



    ####################################################################
    #                        Starting Countdown                        #
    ####################################################################
    for count_down in range(3, 0, -1):
        for i in (x / 10 for x in range(63, -1, -1)):
            # render the screen with the text and the circular timer


            screen.fill(BLUE)

            text = font.render(f'STARTING IN {count_down}', True, GREY)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)

            pygame.draw.arc(screen, WHITE, timer_border, 0, i, 5)
            pygame.display.flip()

            clock.tick(60)
    ###################################################################



    # -------- Main Program Loop -----------
    while not done:
        #
        # EVENT PROCESSING STEP
        #
        # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION
        for event in pygame.event.get(): # User did something.
            if event.type == pygame.QUIT: # If user clicked close.
                done = True # Flag that we are done so we exit this loop.


        # pick a direction and draw the screen

        ####################################################################
        #                        Draw the next instruction                 #
        #                                                                  #
        # Pick a random direction, draw the cicle in the middle,           #
        # and listen for user input                                        #
        ####################################################################
        direction = random.choice(directions)

        text = font.render(direction, True, GREY)
        text_rect = text.get_rect()
        text_rect.center = (WIDTH // 2, HEIGHT // 2)

        for i in (x / 10 for x in range(63, -1, -1)):
            handle_direction(direction)
            screen.fill(BLUE)
            screen.blit(text, text_rect)
            pygame.draw.arc(screen, WHITE, timer_border, 0, i, 5)
            pygame.display.flip()
            time.sleep(0.015)
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


