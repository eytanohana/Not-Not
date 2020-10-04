
# logitech controller gamepad F310 settings
logitech_f310_mappings = {
    'LS_HORIZ': 0, 'LS_VERT': 1, 'TRIGGERS': 2, 'RS_VERT': 3, 'RS_HORIZ': 4,
    'A': 0, 'B': 1, 'X': 2, 'Y': 3,
    'LB': 4, 'RB': 5, 'BACK': 6, 'START': 7,
    'LS_BTN': 8, 'RS_BTN': 9
}

# hats in pygame
d_pad_values = {
    'UP': (0, 1),
    'DOWN': (0, -1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

class GamePad:

    def __init__(self, gamepad, settings):
        self.gamepad = gamepad
        self.settings = dict(settings)

    def dpad(self, i=0):
        return self.gamepad.get_hat(i)

    def is_pressed(self, btn):
        return self.gamepad.get_button(self.settings[btn])

    @property
    def left_stick_horizontal(self):
        return self.gamepad.get_axis(self.settings['LS_HORIZ'])

    @property
    def right_stick_horizontal(self):
        return self.gamepad.get_axis(self.settings['RS_HORIZ'])

    @property
    def left_stick_vertical(self):
        return self.gamepad.get_axis(self.settings['LS_VERT'])

    @property
    def right_stick_vertical(self):
        return self.gamepad.get_axis(self.settings['RS_VERT'])

    @property
    def trigger(self):
        return self.gamepad.get_axis(self.settings['TRIGGERS'])

    # left stick 4 basic directions
    def left_stick_left(self):
        return self.left_stick_horizontal < -0.7

    def left_stick_right(self):
        return self.left_stick_horizontal > 0.7

    def left_stick_up(self):
        return self.left_stick_vertical < -0.7

    def left_stick_down(self):
        return self.left_stick_vertical > 0.7

    # right stick 4 basic directions
    def right_stick_left(self):
        return self.right_stick_horizontal < -0.7

    def right_stick_right(self):
        return self.right_stick_horizontal > 0.7

    def right_stick_up(self):
        return self.right_stick_vertical < -0.7

    def right_stick_down(self):
        return self.right_stick_vertical > 0.7

    def dpad_left(self, i=0):
        return self.dpad(i) == (-1, 0)

    def dpad_right(self, i=0):
        return self.dpad(i) == (1, 0)

    def dpad_up(self, i=0):
        return self.dpad(i) == (0, 1)

    def dpad_down(self, i=0):
        return self.dpad(i) == (0, -1)

