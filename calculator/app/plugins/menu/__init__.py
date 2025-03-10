from calculator.app.commands import Command

class MenuCommand(Command):
    def execute(self):
        # List all available commands
        print("Available commands:")
        print("1. greet - Greet the user")
        print("2. add - Add two numbers")
        print("3. subtract - Subtract two numbers")
        print("4. multiply - Multiply two numbers")
        print("5. divide - Divide two numbers")
        print("6. menu - Show this menu")
        print("7. exit - Exit the application")
        print("8. goodbye - Say goodbye")
