import json
import os
import pickle
import time

import pygame

from modules.direction import Direction
from modules.draw import Colors, GameDrawer
from modules.gamepad import NotNotController

speed = 0.015
ball_speed = 20

score_colors = {
    -1: Colors.GREY,
    0: Colors.BLACK,
    1: Colors.BRONZE,
    2: Colors.SILVER,
    3: Colors.GOLD,
}


def play_game(difficulty):
    """
    Simulate a game a a certain difficulty.

    If the player won the function returns the number
    of lives the player had left: 3, 2, 1, 0.
    The function returns -1 if the player lost.
    """
    lives = 3
    directions = Direction(difficulty=difficulty)
    drawer.bgcolor = Colors.BLUE
    drawer.fill_screen()

    # Starting Countdown
    drawer.display_countdown(3, 'Starting in ')

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
                    return -1

            else:
                drawer.bgcolor = Colors.ORANGE
                drawer.display_lose()
                time.sleep(1)
                return -1

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

        drawer.bgcolor = Colors.BLUE

        for angle in (a / 10 for a in range(63, -1, -1)):
            time.sleep(speed)

            # display the information
            drawer.fill_screen()
            drawer.display_text(directions.target_direction, Colors.GREY)

            drawer.display_text(f'{turn}', offset_x=320, offset_y=-200)

            # draw the ball in the proper place
            drawer.display_ball(ball_pos)
            drawer.display_lives(lives)
            drawer.display_timer(stop_angle=angle)
            drawer.refresh()

            # If the ball reached the end.
            if not drawer.ball_in_border(ball_pos):
                # The player chose correct.
                if directions.correct_direction(input_direction):
                    # Leave the for; go on to the next turn.
                    turn -= 1
                    break

                # The player chose wrong.
                else:
                    drawer.bgcolor = Colors.RED
                    drawer.fill_screen()

                    drawer.display_text('You chose wrong!')
                    drawer.display_lives(lives)
                    drawer.refresh()
                    time.sleep(0.3)
                    # prompt to use a life and play again above
                    lost = True
                    break

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

        # The ball didn't reach the end.
        # The player was too slow and time ran out.
        else:
            drawer.bgcolor = Colors.RED
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
                    time.sleep(0.5)
                    continue

            # End the game
            drawer.bgcolor = Colors.ORANGE
            drawer.display_lose()
            time.sleep(1)
            return -1

    # The player completed the round successfully.
    drawer.bgcolor = Colors.GREEN
    drawer.fill_screen()
    drawer.display_text('Congratulations', Colors.WHITE)
    drawer.refresh()
    time.sleep(2)
    return lives


if __name__ == '__main__':
    # Set up the drawer object
    drawer = GameDrawer(800, 500, 'NOT NOT')
    # Icons made by <a href="https://www.flaticon.com/authors/pixel-buddha" title="Pixel Buddha">Pixel Buddha</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>')
    icon = pygame.image.load('static/exclamation-mark.png')
    pygame.display.set_icon(icon)

    # flags
    running = True

    # Used to manage how fast the screen updates.
    clock = pygame.time.Clock()

    # Initialize the joysticks.
    pygame.joystick.init()

    # Gamepad settings - try to load, but allow keyboard-only play
    gamepad_settings = {}
    try:
        with open('logitechF310-mappings.json') as f:
            gamepad_settings = json.load(f)
    except FileNotFoundError:
        print('Gamepad settings file not found. Using keyboard arrow keys only.')

    # Try to initialize gamepad, but allow keyboard-only play
    if pygame.joystick.get_count() > 0:
        try:
            gamepad = NotNotController(pygame.joystick.Joystick(0), gamepad_settings)
            print('Gamepad connected. You can use gamepad or arrow keys.')
        except Exception as e:
            print(f'Error initializing gamepad: {e}. Using keyboard arrow keys only.')
            gamepad = NotNotController(None, gamepad_settings)
    else:
        print('No gamepad detected. Using keyboard arrow keys.')
        gamepad = NotNotController(None, gamepad_settings)

    if not os.path.exists('.game_history'):
        game_history = {}

    else:
        with open('.game_history', 'rb') as f:
            game_history = pickle.load(f)
            print(game_history)

    right_arrow = pygame.image.load('static/arrow-pointing-to-right.png')
    left_arrow = pygame.image.load('static/arrow-pointing-to-left.png')

    level = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        try:
            levels_beaten = max(game_history)
        except ValueError:
            levels_beaten = -1

        drawer.bgcolor = Colors.BLUE

        ########################################################
        #              Display Available Levels                #
        ########################################################
        display_rounds = True

        while display_rounds:
            score_at_level = game_history.get(level, -1)
            round_color = score_colors[score_at_level]

            drawer.display_round(level, round_color=round_color)
            drawer.display_text('Press down to play', offset_y=180)
            drawer.display_text('Press up to quit', offset_y=-180)

            # display left/right arrows
            if level > 0:
                drawer.display_arrow(left_arrow, (30, drawer.height // 2 - 128 // 2))
                left_round_color = score_colors.get(game_history.get(level - 1, -1))
            if level <= levels_beaten:
                drawer.display_arrow(
                    right_arrow,
                    (drawer.width - 128 - 30, drawer.height // 2 - 128 // 2),
                )
                right_round_color = score_colors.get(game_history.get(level + 1, -1))
            drawer.refresh()

            # get user input
            pygame.event.get()
            while (input_direction := gamepad.direction_input()) is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                if not running:
                    break

            if not running:
                break

            if input_direction == 'LEFT':
                if level <= 0:
                    drawer.shake_round(0, round_color=round_color)
                else:
                    drawer.switch_rounds(-1, level, round_color=[round_color, left_round_color])
                    level -= 1

            if input_direction == 'RIGHT':
                # display the next round
                if level <= levels_beaten:
                    drawer.switch_rounds(1, level, round_color=[round_color, right_round_color])
                    level += 1
                else:
                    drawer.shake_round(level)

            # quit
            if input_direction == 'UP':
                running = False
                break

            if input_direction == 'DOWN':
                difficulty = level
                break

        ########################################################
        #               End Displaying Rounds                  #
        ########################################################
        if not running:
            break

        won = play_game(difficulty)
        if won == -1:
            print(f'Game {difficulty} lost')
        else:
            print(f'Game {difficulty} won using {3 - won} lives.')
            if game_history.get(difficulty, -1) < won:
                game_history[difficulty] = won
                with open('.game_history', 'wb') as f:
                    pickle.dump(game_history, f)

        time.sleep(0.2)
