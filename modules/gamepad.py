class Gamepad:

    def __init__(self, gamepad, settings):
        gamepad.init()
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


class NotNotController(Gamepad):

    def left(self):
        return (self.dpad_left() or self.left_stick_left() or
                self.right_stick_left() or self.is_pressed('X'))

    def right(self):
        return (self.dpad_right() or self.left_stick_right() or
                self.right_stick_right() or self.is_pressed('B'))

    def up(self):
        return (self.dpad_up() or self.left_stick_up() or
                self.right_stick_up() or self.is_pressed('Y'))

    def down(self):
        return (self.dpad_down() or self.left_stick_down() or
                self.right_stick_down() or self.is_pressed('A'))

    def direction_input(self):
        if self.left():
            return 'LEFT'

        elif self.right():
            return 'RIGHT'

        elif self.up():
            return 'UP'

        elif self.down():
            return 'DOWN'

        else:
            return None
