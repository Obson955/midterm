"""Clear history command plugin for the calculator."""

from calculator.app.commands import Command
from calculator.history import HistoryManager

class ClearHistoryCommand(Command):
    """Command to clear calculation history."""
    
    def execute(self):
        """Execute the clear history command."""
        confirmation = input("Are you sure you want to clear the calculation history? (y/n): ").strip().lower()
        
        if confirmation == 'y':
            HistoryManager.clear_history()
            print("History cleared successfully.")
        else:
            print("Operation cancelled.")
