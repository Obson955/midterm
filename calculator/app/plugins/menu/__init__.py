from calculator.app.commands import Command
from calculator.logging_config import get_logger

logger = get_logger(__name__)

class MenuCommand(Command):
    def execute(self):
        # List all available commands
        logger.info("Menu command executed")
        
        print("\nCalculator Menu")
        print("\nBasic Operations:")
        print("add - Add two numbers")
        print("subtract - Subtract two numbers")
        print("multiply - Multiply two numbers")
        print("divide - Divide two numbers")
        
        print("\nHistory Management:")
        print("history - View calculation history")
        print("save_history - Save calculation history to a file")
        print("load_history - Load calculation history from a file")
        print("clear_history - Clear calculation history")
        print("delete_history - Delete history file")
        
        print("\nAdvanced Features:")
        print("statistics - View statistical analysis of calculations")
        print("export_excel - Export calculation history to Excel")
        print("filter_history - Filter calculation history")
        
        print("\nApplication Control:")
        print("menu - Show this menu")
        print("exit - Exit the application")
