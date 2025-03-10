from calculator.app.commands import Command


class GoodbyeCommand(Command):
    def execute(self):
        print("Goodbye")