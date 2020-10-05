import pygame
import json
import random
import time
import threading
from queue import Queue
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

moves = ['left', 'right', 'up', 'down']

def draw_next():
    move = random.choice(moves)
    text = font.render(move, True, GREY)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    for i in (x / 10 for x in range(63, -1, -1)):
        screen.fill(BLUE)
        screen.blit(text, text_rect)
        pygame.draw.arc(screen, WHITE, timer_border, 0, i, 5)
        pygame.display.flip()
        time.sleep(0.015)

def handle_input(gamepad, inputs):
    while True:
        print('handling')
        print(gamepad.is_pressed('A'))
        if gamepad.is_pressed('A'):
            print('putting A')
            inputs.put('A')
        time.sleep(.005)

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
        #
        #
        ####################################################################
        # inputs_queue = Queue()
        draw_thread = threading.Thread(target=draw_next)
        # input_thread = threading.Thread(target=handle_input, args=(logitech_gamepad, inputs_queue))
        draw_thread.start()
        # input_thread.start()

        while draw_thread.is_alive():
            print('hello')
            print(logitech_gamepad.is_pressed('A'))
            # btn = inputs_queue.get()
            # print(btn)

        

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


