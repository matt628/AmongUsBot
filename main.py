# making screenshot
import pyscreenshot as ImageGrab

# moving mouse
import pyautogui

# named tuples - more readable code
from collections import namedtuple

# activating after key press
import keyboard

import time

# config dicts - initial data
'''
You just need to check the position of cabels on your screen and fill below values. 
'''
config_wires = {
    'left_column_x': 560,
    'right_column_x': 1345,
    '1_row_y': 274,
    '2_row_y': 459,
    '3_row_y': 646,
    '4_row_y': 833,
}

config_key = {
    'run_wire_bot': '1'
}

# data structures
Point = namedtuple('Point', 'x y')
Connection = namedtuple('Connection', 'left_wire right_wire')


# program data
left_wires_colors = []
right_wires_colors = []
left_wires = [
    Point(config_wires['left_column_x'], config_wires['1_row_y']),
    Point(config_wires['left_column_x'], config_wires['2_row_y']),
    Point(config_wires['left_column_x'], config_wires['3_row_y']),
    Point(config_wires['left_column_x'], config_wires['4_row_y']),
]
right_wires = [
    Point(config_wires['right_column_x'], config_wires['1_row_y']),
    Point(config_wires['right_column_x'], config_wires['2_row_y']),
    Point(config_wires['right_column_x'], config_wires['3_row_y']),
    Point(config_wires['right_column_x'], config_wires['4_row_y']),
]


# instructions

def take_screenshot():
    im = ImageGrab.grab()
    return im


def move_mouse(from_x, from_y, to_x, to_y):
    pyautogui.moveTo(from_x, from_y)
    pyautogui.dragTo(to_x, to_y, button='left', duration=0.47)
    # movment duration is set to 0.47 second. If it's less wires cant't be dragged

# 'Computer vision'


def check_color(x, y, im):
    color = im.getpixel((x, y))
    print(color)
    return color


'''
This functions analyze cabels color layout.
It fills `left_wires_colors` and `right_wire_colors` arrays with apropiate colors
'''


def analyze_screenshot(screenshot):
    for wire in left_wires:
        left_wires_colors.append(check_color(wire.x, wire.y, screenshot))
    for wire in right_wires:
        right_wires_colors.append(check_color(wire.x, wire.y, screenshot))


'''
This function based on wire colors array return information
how wires should be conected
@return: [(left_wire_point right_wire_point), ...]
'''


def figure_way_to_connect():
    point_pairs = []
    for left_index, color in enumerate(left_wires_colors):
        right_index_of_same_color = right_wires_colors.index(color)
        connection = Connection(
            left_wires[left_index], right_wires[right_index_of_same_color])
        point_pairs.append(connection)
    return point_pairs


'''
Function connects wire on screen
'''


def connect_wires(connection_array):
    for connection in connection_array:
        move_mouse(connection.left_wire.x, connection.left_wire.y,
                   connection.right_wire.x, connection.right_wire.y)


def run_wire_bot(e):
    screenshot = take_screenshot()
    analyze_screenshot(screenshot)
    connection_array = figure_way_to_connect()
    connect_wires(connection_array)
    global left_wires_colors, right_wires_colors
    left_wires_colors = []
    right_wires_colors = []


def main():
    keyboard.on_press_key(config_key['run_wire_bot'], run_wire_bot) 
    # above line requreies to run pythhon script in background 
    # you can achive that by running this script in interactive mode -> python -i main.py

    # await for key press
    # while(True):    
    #     if keyboard.is_pressed(config_key['run_wire_bot']):
    #         run_wire_bot()
    #         time.sleep(300)


if __name__ == '__main__':
    main()
