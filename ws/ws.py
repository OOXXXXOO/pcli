import argparse
import yaml
import subprocess
import sys
from colorama import Fore, Style

ascii_art = """
\033[91m __          _______        _____ _      _____ \033[0m
\033[92m \ \        / / ____|      / ____| |    |_   _|\033[0m
\033[93m  \ \  /\  / / (___ ______| |    | |      | |  \033[0m
\033[94m   \ \/  \/ / \___ \______| |    | |      | |  \033[0m
\033[95m    \  /\  /  ____) |     | |____| |____ _| |_ \033[0m
\033[96m     \/  \/  |_____/       \_____|______|_____|\033[0m
"""


def load_config():
    with open('ws/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def execute_command(command_type, script):
    print(f"Executing {command_type} command: {script}")
    try:
        if command_type == "system":
            subprocess.call(script, shell=True)
        elif command_type == "python":
            exec(open(script).read())
        elif command_type == "bash":
            subprocess.call(["bash", script])
        elif command_type == "binary":
            subprocess.call([script])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    print(ascii_art)

    config = load_config()

    parser = argparse.ArgumentParser(description="Custom command system")
    subparsers = parser.add_subparsers(dest="command")

    for cmd, info in config["commands"].items():
        cmd_parser = subparsers.add_parser(cmd, help=info["help"])
        cmd_parser.add_argument("-?", "--show-help", action="store_true", help="Show help for subcommands")
        subcommand_parsers = cmd_parser.add_subparsers(dest="subcommand")

        for subcmd, subinfo in info["subcommands"].items():
            subcommand_parser = subcommand_parsers.add_parser(subcmd, help=subinfo["help"])
            subcommand_parser.set_defaults(command=cmd, subcommand=subcmd, type=subinfo["type"])

    args = parser.parse_args()

    if args.command:
        command_info = config["commands"][args.command]
        subcommand_info = command_info["subcommands"].get(args.subcommand)
        if args.show_help or not subcommand_info:
            print(f"Usage: ws {args.command} <subcommand>")
            print(f"{command_info['help']}\n")
            print("Available subcommands:")
            for subcmd, subinfo in command_info["subcommands"].items():
                print(f"  {subcmd}: {subinfo['help']}")
        elif subcommand_info:
            print(f"Command: ws {args.command} {args.subcommand}")
            print(f"Description: {subcommand_info['help']}")
            print(f"Color: {Fore.__dict__[subcommand_info['color']]}")

            execute_command(subcommand_info["type"], subcommand_info["script"])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

