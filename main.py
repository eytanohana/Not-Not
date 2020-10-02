import pygame
import random
from inputs import get_gamepad
import time


WIDTH = 800
HEIGHT = 500

BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (77,) * 3

RADIUS = 5
border = 400

moves = ['left', 'right', 'up', 'down']

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NOT NOT')

    border_rect = pygame.Rect((WIDTH - border) // 2, (HEIGHT - border) // 2, border, border)
    font = pygame.font.SysFont('comicsansms', 60)

    while 1:

        move = random.choice(moves)

        for i in (x / 10 for x in range(63, -1, -1)):
            # render the screen with the text and the circular timer
            screen.fill(BLUE)

            text = font.render(move, True, GREY)
            text_rect = text.get_rect()
            text_rect.center = (WIDTH // 2, HEIGHT // 2)
            screen.blit(text, text_rect)

            pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), RADIUS)

            pygame.draw.arc(screen, WHITE, border_rect, 0, i, 5)
            time.sleep(.015)

            pygame.display.flip()





