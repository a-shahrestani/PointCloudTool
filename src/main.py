import os
from pathlib import Path

import laspy
import pandas as pd
from laspy import LaspyException
from plyfile import PlyData

_point_cloud_actions = {1: 'reduce intensity',
                        2: 'export CSV',
                        3: 'export LAZ',
                        4: 'export LAS',
                        5: 'export PLY',
                        6: 'standardize the classes'}


def _general_action_selection(state):
    general_actions = {1: 'read LAS file',
                       2: 'read PLY file',
                       3: 'read CSV file'
                       }
    print(f'What are you looking to do: \n')
    for action in general_actions.items():
        print(f'{str(action[0])}. {str(action[1])}')
    command = input('Enter your command: ')
    if int(command) not in general_actions.keys():
        print('Wrong Command! Please choose a command from the command list!')
        return 0
    else:
        return state * 10 + int(command)


def _enter_file_address():
    address = input('Enter the complete address of the file: ')
    address = Path(address)
    return address


def _read_las_file(state):
    address = _enter_file_address()
    os.system('clear')
    try:
        las_file = laspy.read(address)
    except OSError as e1:
        print(f'No such file or directory: {address}')
        print(f'Please enter a valid address')
        return state
    except LaspyException as e2:
        print('The file you have chosen does not have a valid format. Please check your file and redo the operations')
        return 1
    return las_file, 2


def _read_ply_file(state):
    address = _enter_file_address()
    ply_file = PlyData.read(address)
    return ply_file, 2


def _read_csv_file(state):
    address = _enter_file_address()
    csv_file = pd.read_csv(address)
    return csv_file, 2


def _initial_greetings(state):
    print('Welcome to the PointCloudTool!')
    state = _general_action_selection(state)
    os.system('clear')
    return state


def _point_cloud_action_selection(state):
    point_cloud_actions = {1: 'reduce intensity',
                           2: 'export CSV',
                           3: 'export LAZ',
                           4: 'export LAS',
                           5: 'export PLY',
                           6: 'standardize the classes'}
    print(f'What are you looking to do: \n')
    for action in point_cloud_actions.items():
        print(f'{str(action[0])}. {str(action[1])}')
    command = input('Enter your command: ')
    if command not in point_cloud_actions.keys():
        print('Wrong Command! Please choose a command from the command list!')
        return 0
    else:
        return state * 10 + int(command)


if __name__ == '__main__':
    stage = 1
    while stage != 6:
        if stage == 1:  # initial command
            stage = _initial_greetings(stage)
        elif stage == 11:  # read LAS
            stage = _read_las_file(stage)
        elif stage == 12:  # read PLY
            stage = _read_ply_file(stage)
        elif stage == 13:  # read CSV
            stage = _read_csv_file(stage)
        elif stage == 2:  # point cloud command
            stage = _point_cloud_action_selection(stage)
