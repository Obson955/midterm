"""Load history command plugin for the calculator."""

from calculator.app.commands import Command
from calculator.history import HistoryManager

class LoadHistoryCommand(Command):
    """Command to load calculation history from a file."""
    
    def execute(self):
        """Execute the load history command."""
        file_path = input("Enter file path to load history (or press Enter for default): ").strip()
        
        if not file_path:
            file_path = None  # Use default path
            
        success = HistoryManager.load_history(file_path)
        
        if success:
            print("History loaded successfully.")
        else:
            print(f"Error loading history. File may not exist or is invalid.")
