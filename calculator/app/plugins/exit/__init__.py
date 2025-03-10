import sys
from calculator.app.commands import Command


class ExitCommand(Command):
    def execute(self):
        sys.exit("Exiting...")