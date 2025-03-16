from calculator.app.commands import Command
from calculator.logging_config import get_logger

logger = get_logger(__name__)

class MenuCommand(Command):
    def execute(self):
        # List all available commands
        logger.info("Menu command executed")
        
        print("\n===== Calculator Application =====")
        print("\nBasic Operations:")
        print("1. add - Add two numbers")
        print("2. subtract - Subtract two numbers")
        print("3. multiply - Multiply two numbers")
        print("4. divide - Divide two numbers")
        
        print("\nHistory Management:")
        print("5. history - View calculation history")
        print("6. save_history - Save calculation history to a file")
        print("7. load_history - Load calculation history from a file")
        print("8. clear_history - Clear calculation history")
        print("9. delete_history - Delete history file")
        
        print("\nAdvanced Data Features:")
        print("10. statistics - View statistical analysis of calculations")
        print("11. export_excel - Export calculation history to Excel with statistics")
        print("12. filter_history - Filter calculation history by various criteria")
        
        print("\nApplication Commands:")
        print("13. menu - Show this menu")
        print("14. exit - Exit the application")
        print("15. goodbye - Say goodbye")
        print("16. greet - Greet the user")
