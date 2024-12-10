import os

import keyboard

custom_handlers = {
    "py-pr": lambda c: keyboard.press_and_release(c)
}

def parse_command_sequence(key, value):
    command_sequence = list(value)

    return key, command_sequence

def execute_command(command: str):
    for prefix in custom_handlers:
        if not command.startswith(prefix):
            continue

        command = command.removeprefix(prefix).strip()
        custom_handlers[prefix](command)
        return
    os.system(command)

def execute_command_sequence(command_sequence):
    for command in command_sequence:
        execute_command(command)


def execute(config):
    for key, value in config.items():
        hotkey, command_sequence = parse_command_sequence(key, value)
        keyboard.add_hotkey(hotkey, execute_command_sequence, args=[command_sequence])
    pass
