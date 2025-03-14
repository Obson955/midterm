"""Delete history file command plugin."""

from calculator.app.commands import Command
from calculator.history import HistoryManager
import os

class DeleteHistoryCommand(Command):
    """Command to delete a history file."""
    
    def execute(self):
        """Execute the delete history file command."""
        file_path = input("Enter the path to the history file (or press Enter for default): ")
        if not file_path:
            file_path = "calculation_history.csv"
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{file_path}'? (y/n): ")
        if confirm.lower() != 'y':
            print("Operation canceled.")
            return
        
        # Delete history file
        if HistoryManager.delete_history_file(file_path):
            print(f"History file deleted: {file_path}")
        else:
            print(f"Error: Could not delete history file '{file_path}'.")
