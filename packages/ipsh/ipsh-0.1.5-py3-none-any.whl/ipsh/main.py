# -*- coding: utf-8 -*-

"""
ipsh main cli script
"""

import argparse
import logging
import sys

# import typer

# from typing_extensions import Annotated

from . import __version__
from . import interpreters
from . import interactive

# app = typer.Typer()

COMMAND_DEMO = "demo"
COMMAND_SHOWKEYS = "showkeys"


def get_arguments(*args: str, test_context: bool = False) -> argparse.Namespace:
    """Get commandline arguments"""
    main_parser = argparse.ArgumentParser(
        prog="ipsh", description="interactive pseudo shell command line interface"
    )
    main_parser.set_defaults(loglevel=logging.INFO)
    main_parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        help="debug mode",
    )
    main_parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="print version and exit",
    )
    subparsers = main_parser.add_subparsers(required=True)
    demo_parser = subparsers.add_parser(COMMAND_DEMO, help="demonstrate a pseudo shell")
    demo_parser.set_defaults(command=COMMAND_DEMO)
    demo_parser.add_argument(
        "-s",
        "--simple",
        action="store_true",
        help="show the simplest form using a dummy interpreter",
    )
    showkeys_parser = subparsers.add_parser(
        COMMAND_SHOWKEYS,
        help="loop and show key codes until CTRL-C or CTRL-D is pressed",
    )
    showkeys_parser.set_defaults(command=COMMAND_SHOWKEYS)
    if not test_context or not args:
        args_to_parse: list[str] | None = None
    else:
        args_to_parse = list(args)
    #
    return main_parser.parse_args(args=args_to_parse)


def run(*args: str, test_context: bool = False) -> int:
    """Run the main program"""
    arguments = get_arguments(*args, test_context=test_context)
    logging.basicConfig(format="[%(levelname)s] %(message)s", level=arguments.loglevel)
    if arguments.command == COMMAND_DEMO:
        if arguments.simple:
            interpreter = interpreters.BaseInterpreter()
            description = "simple PseudoShell demo"
        else:
            interpreter = interpreters.ArgumentBasedInterpreter()
            description = "PseudoShell demo with an argparse based interpreter"
        #
        logging.info("Running %s", description)
        interactive.PseudoShell(prompt=" > ", interpreter=interpreter).run()
    elif arguments.command == COMMAND_SHOWKEYS:
        logging.info("Running showkeys subcommand")
        logging.info("Exit with CTRL-C or CTRL-D")
        while True:
            key = interactive.getkey()
            print([hex(ord(char)) for char in key])
            if key in (interactive.CTRL_C, interactive.CTRL_D):
                break
            #
        #
    #
    return 0


def app():
    """app function"""
    sys.exit(run())
