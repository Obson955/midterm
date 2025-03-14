"""Delete history file command plugin for the calculator."""

from calculator.app.commands import Command
from calculator.history import HistoryManager

class DeleteHistoryFileCommand(Command):
    """Command to delete the history file."""
    
    def execute(self):
        """Execute the delete history file command."""
        file_path = input("Enter file path to delete (or press Enter for default): ").strip()
        
        if not file_path:
            file_path = None  # Use default path
            
        confirmation = input(f"Are you sure you want to delete the history file? This cannot be undone. (y/n): ").strip().lower()
        
        if confirmation == 'y':
            success = HistoryManager.delete_history_file(file_path)
            
            if success:
                print("History file deleted successfully.")
            else:
                print("Error deleting history file. File may not exist or is protected.")
        else:
            print("Operation cancelled.")
