import argparse
from time import sleep

from burningkeys import example_config, read_config, execute_config

def main():
    parser = argparse.ArgumentParser(prog="bkeys", description="Burningkeys is a lightweight python script to invoke "
                                                               "certain commands using hotkeys. This cli is meant mainly for coding."
                                                               "For example you might be editing in a basic text editor and would"
                                                               "like to invoke a linter on your project. Well now you can set that up")

    parser.add_argument("--create-example", action="store_true")

    args = parser.parse_args()

    if args.create_example:
        example_config.create()
        return

    config = read_config.config()
    execute_config.execute(config)

    while True:
        sleep(1)


def command_entry_point():
    try:
        main()
    except KeyboardInterrupt:
        print("Program was interrupted by user")