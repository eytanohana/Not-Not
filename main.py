import pygame
from inputs import get_gamepad

WIDTH = 800
HEIGHT = 500

BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

RADIUS = 5

moves = {'left', 'right', 'up', 'down'}

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLUE)

    pygame.draw.circle(screen, WHITE, (WIDTH//2, HEIGHT//2), RADIUS)

    while True:
        pygame.display.flip()





