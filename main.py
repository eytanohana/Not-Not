import pygame
import random
from inputs import get_gamepad


WIDTH = 800
HEIGHT = 500

BLUE = (12, 133, 127)
WHITE = (255, 255, 255)
GREY = (77,) * 3

RADIUS = 5

moves = ['left', 'right', 'up', 'down']

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NOT NOT')

    screen.fill(BLUE)



    print(pygame.font.get_fonts())

    font = pygame.font.SysFont('comicsansms', 60)
    text = font.render(random.choice(moves), True, GREY)
    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)

    pygame.draw.circle(screen, WHITE, (WIDTH // 2, HEIGHT // 2), RADIUS)

    pygame.display.flip()

    while 1:
        pass





