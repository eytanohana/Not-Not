import pygame

# Define some colors.
BLACK = (0,) * 3
RED = (255, 0, 0)
BLUE = (12, 133, 127)
WHITE = (255,) * 3
GREY = (77,) * 3
GREEN = (11, 212, 51)
ORANGE = (230, 163, 48)
GOLD = (255, 215, 0)
BRONZE = (205, 127, 50)
SILVER = (192, 192, 192)

class GameDrawer:

    def __init__(self, width, height, caption, font_name=None, font_size=60):
        self.width = width
        self.height = height
        self.caption = caption

        pygame.init()
        self._font = pygame.font.SysFont(font_name, font_size)
        self._bgcolor = BLUE
        self.screen = pygame.display.set_mode((width, height))

        length = 450
        self._timer_bounds = pygame.Rect((self.width - length) // 2, (self.height - length) // 2, length, length)
        pygame.display.set_caption(caption)

        self.clock = pygame.time.Clock()

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

    def display_timer(self, start_angle=0, stop_angle=0, color=WHITE, width=5):
        pygame.draw.arc(self.screen, color, self._timer_bounds, start_angle, stop_angle, width)

    def display_text(self, text, color=BLACK, offset_x=0, offset_y=0):
        text = self.font.render(text, True, color)
        text_rect = text.get_rect()

        position = [self.width // 2 + offset_x, self.height // 2 + offset_y]
        text_rect.center = position
        self.screen.blit(text, text_rect)

    def display_option(self, text):
        self.fill_screen()
        self.display_text(text)
        self.display_text('<- ok       no thanks->', offset_y=50)
        self.refresh()

    def display_lose(self):
        self.fill_screen()
        self.display_text('YOU LOST')
        self.refresh()

    def display_countdown(self, rounds, text):
        for count_down in range(rounds, 0, -1):
            # in radians 2pi, pi, 0

            for angle in (a / 10 for a in range(0, 63, 1)):

                # Color the screen
                self.fill_screen()
                # Draw the countdown
                self.display_text(text + str(count_down), GREY)
                # Draw the circular timer
                self.display_timer(angle-1, angle)
                # Flip
                self.refresh()
                # 60 fps
                self.clock.tick(60)

    def display_lives(self, lives):
        for i in range(lives):
            pygame.draw.circle(self.screen, WHITE, (30 * (i + 1), 30), 10)

    def ball_in_border(self, ball_pos):
        padding = 5
        return (self._timer_bounds.left + padding < ball_pos[0] < self._timer_bounds.right - padding
                and self._timer_bounds.top + padding < ball_pos[1] < self._timer_bounds.bottom - padding)

    def display_round(self, round, round_color=BLACK, text_color=WHITE, offset=0, fill_screen=True):
        if fill_screen:
            self.fill_screen()
        length = 250
        rect = pygame.Rect((self.width - length) // 2 + offset, (self.height - length) // 2, length, length)
        pygame.draw.rect(self.screen, round_color, rect)

        self.display_text(f'ROUND {round}', text_color, offset_x=offset)

    def shake_round(self, round, round_color=BLACK, text_color=WHITE):
        shake_weight = 20
        for i in range(3):
            for offset in range(shake_weight):
                self.display_round(round, round_color=round_color, text_color=text_color, offset=offset)
                self.refresh()

            for offset in range(shake_weight, -shake_weight, -1):
                self.display_round(round, round_color=round_color, text_color=text_color, offset=offset)
                self.refresh()

            for offset in range(-shake_weight, 0, 1):
                self.display_round(round, round_color=round_color, text_color=text_color, offset=offset)
                self.refresh()

    def switch_rounds(self, direction, level, round_color=BLACK, text_color=WHITE):

        if isinstance(round_color, list):
            round_color, next_round_color = round_color
        else:
            next_round_color = BLACK

        if direction > 0:

            for offset in range(self.width//2):
                self.fill_screen()
                self.display_round(level, round_color=round_color, text_color=text_color, offset=-offset, fill_screen=False)
                self.display_round(level + 1, round_color=next_round_color, offset=self.width - offset * 2, fill_screen=False)
                self.refresh()

        else:
            for offset in range(self.width//2):
                self.fill_screen()
                self.display_round(level, round_color=round_color, text_color=text_color, offset=offset, fill_screen=False)
                self.display_round(level - 1, round_color=next_round_color, text_color=text_color, offset=-self.width//2 + offset, fill_screen=False)
                self.refresh()

    def display_arrow(self, arrow, pos):
        self.screen.blit(arrow, pos)
