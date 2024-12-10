# -*- coding: utf-8 -*-
"""
interpreters module
"""

import argparse
import logging
import shlex

from .buffers import History


CMD_EXIT = "exit"
CMD_HELP = "help"
CMD_HISTORY = "history"
CMD_QUIT = "quit"

COMMON_DESCRIPTIONS = {
    CMD_EXIT: "Exit the interpreter",
    CMD_HELP: "Print help message",
    CMD_QUIT: "Exit the interpreter",
    CMD_HISTORY: "Show the command history",
}


class InterpreterExit(Exception):
    """Raised on Interpreter exit"""


class NoSuggestionFound(Exception):
    """Raised if no suggestion could be found for the given line"""


class BaseInterpreter:
    """Shell interpreter base class"""

    stopcommands: tuple[str, ...] = CMD_EXIT, CMD_QUIT

    def __init__(self, history: History = History()) -> None:
        """Initialize the interpreter"""
        self.history = history
        self.known_commands = {CMD_HISTORY} | set(self.stopcommands)

    def execute(self, read_line: str) -> None:
        """Execute the read line and return a Reaction instance"""
        core_line = read_line.strip()
        logging.debug("Executing %r ...", core_line)
        if core_line in self.stopcommands:
            raise InterpreterExit
        #
        self.history.add(read_line)
        if core_line.startswith(CMD_HISTORY):
            self.show_history(start=1, end=-1)
        #

    def show_history(self, start=1, end=-1) -> None:
        """Show the history range"""
        logging.info("History:")
        for idx, entry in self.history.iter_range(start, end):
            print(f"  [{idx:3d}]  {entry}")
        #

    def suggest(self, line) -> str:
        """Suggest an entry if line matches the beginning of exact one entry
        If line matches two or more beginnings, suggest the
        longest common beginning.
        """
        filtered = {
            suggestion
            for suggestion in self.known_commands
            if suggestion.startswith(line)
        }
        if not filtered:
            raise NoSuggestionFound
        #
        if len(filtered) == 1:
            return f"{filtered.pop()} "
        #
        # Find the longest common match between the remaining suggestions
        common = line
        suggestion = common
        while True:
            pos = len(common)
            for idx, entry in enumerate(filtered):
                if not idx:
                    try:
                        suggestion = f"{common}{entry[pos]}"
                    except IndexError:
                        return common
                    #
                    continue
                #
                if not entry.startswith(suggestion):
                    return common
                #
            #
            common = suggestion
        #
        raise NoSuggestionFound


class ArgumentBasedInterpreter(BaseInterpreter):
    """argparse based interpreter"""

    def __init__(self, history: History = History(), **kwargs) -> None:
        """Initialize the interpreter"""
        super().__init__(history=history)
        self.descriptions = dict(COMMON_DESCRIPTIONS) | kwargs
        self.known_commands = set(self.descriptions)
        self.__cmd_parser = argparse.ArgumentParser(
            prog="", description=None, add_help=False, exit_on_error=False
        )
        self.__subparser = self.__cmd_parser.add_subparsers()
        self.__commands: dict[str, argparse.ArgumentParser] = {}
        for command, desc in self.descriptions.items():
            self.__commands[command] = self.__subparser.add_parser(
                command,
                help=desc,
                description=desc,
                add_help=False,
                exit_on_error=False,
            )
            self.__commands[command].set_defaults(command=command)
        #
        self[CMD_HELP].add_argument("topic", nargs="?", help="the help topic")
        self[CMD_HISTORY].add_argument(
            "-n",
            "--number",
            type=int,
            help="Number of history entries to show (default is all)",
        )

    def __getitem__(self, command: str):
        """Return the parser for _command_"""
        return self.__commands[command]

    def dispatch(self, arguments: argparse.Namespace):
        """Override this method for the real action"""
        logging.debug("Executing %r", arguments)
        if arguments.command == CMD_HELP:
            try:
                parser = self[arguments.topic]
            except KeyError:
                self.__cmd_parser.print_help()
            else:
                parser.print_help()
            #
            return
        #
        if arguments.command == CMD_HISTORY:
            if arguments.number:
                start = -arguments.number
            else:
                start = 1
            #
            super().show_history(start=start)
            return
        #

    def execute(self, read_line: str) -> None:
        """Execute the read line and return a Reaction instance"""
        logging.debug("Executing %r ...", read_line)
        try:
            arguments = self.__cmd_parser.parse_args(shlex.split(read_line))
        except argparse.ArgumentError as error:
            logging.error(str(error))
            return
        #
        if arguments.command in self.stopcommands:
            raise InterpreterExit
        #
        self.history.add(read_line)
        self.dispatch(arguments)
