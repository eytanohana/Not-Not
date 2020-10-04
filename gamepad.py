import pygame

event_codes = {
        'ABS_RZ': 'RT',  # right trigger: 0 - 255
        'ABS_Z': 'LT',  # left trigger : 0 - 255
        'BTN_TL': 'LB',  # left button  : 0 or 1
        'BTN_TR': 'RB',  # right button : 0 or 1
        'ABS_HAT0Y': 'D_VERT',  # D pad up down: up -1 down 1
        'ABS_HAT0X': 'D_HORIZ',  # D pad left right: left -1 right 1
        'BTN_EAST': 'B',  # B : 0 or 1
        'BTN_SOUTH': 'A',  # A : 0 or 1
        'BTN_WEST': 'X',  # X : 0 or 1
        'BTN_NORTH': 'Y',  # Y : 0 or 1
        'ABS_RX': 'RS_HORIZ',  # right stick left right: center 128 right 32767 left -32768
        'ABS_RY': 'RS_VERT',  # right stick up down: center 128 up 32767 down -32768
        'ABS_X': 'LS_HORIZ',  # left stick left right: center 128 right 32767 left -32768
        'ABS_Y': 'LS_VERT',  # left stick up down: center 128 up 32767 down -32768
        'BTN_THUMBR': 'RS_BTN',  # right stick button: pressed 1 unpressed 0
        'BTN_THUMBL': 'LS_BTN',  # left stick button: pressed 1 unpressed 0
        'BTN_SELECT': 'START',  # start button: pressed 1 unpressed 0
        'BTN_START': 'BACK',  # back button: pressed 1 unpressed 0
    }