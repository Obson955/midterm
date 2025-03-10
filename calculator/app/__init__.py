import pkgutil
import importlib
from calculator.app.commands import CommandHandler, Command
from calculator.app.commands.command_handler import CalculatorCommand

class App:
    def __init__(self):
        self.command_handler = CommandHandler()

    def load_plugins(self):
        # Dynamically load all plugins in the plugins directory
        plugins_package = 'calculator.app.plugins'
        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_package.replace('.', '/')]):
            if is_pkg:  # Ensure it's a package
                plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                for item_name in dir(plugin_module):
                    item = getattr(plugin_module, item_name)
                    try:
                        if issubclass(item, (Command)) and item is not Command:  # Changed this line
                            self.command_handler.register_command(plugin_name, item())
                    except TypeError:
                        continue  # If item is not a class or unrelated class, just ignore

    def start(self):
        """Start the application loop."""
        self.load_plugins()
        print("Welcome to the calculator! Type 'exit' to quit.")
        self.command_handler.execute_command("menu")
        
        while True:
            command = input(">>> ").strip()
            if command.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
            self.command_handler.execute_command(command)