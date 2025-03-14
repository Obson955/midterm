"""Save history command plugin for the calculator."""

from calculator.app.commands import Command
from calculator.history import HistoryManager

class SaveHistoryCommand(Command):
    """Command to save calculation history to a file."""
    
    def execute(self):
        """Execute the save history command."""
        file_path = input("Enter file path to save history (or press Enter for default): ").strip()
        
        if not file_path:
            file_path = None  # Use default path
            
        try:
            saved_path = HistoryManager.save_history(file_path)
            print(f"History saved successfully to: {saved_path}")
        except Exception as e:
            print(f"Error saving history: {e}")
