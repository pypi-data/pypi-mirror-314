import os

import keyboard


def parse_command_sequence(key, value):
    command_sequence = list(value)

    return key, command_sequence


def execute_command_sequence(command_sequence):
    for command in command_sequence:
        # run(shlex.split(command))
        os.system(command)


def execute(config):
    for key, value in config.items():
        hotkey, command_sequence = parse_command_sequence(key, value)
        keyboard.add_hotkey(hotkey, execute_command_sequence, args=[command_sequence])
    pass
