"""History command plugin for the calculator."""

from calculator.app.commands import Command
from calculator.history import HistoryManager
import pandas as pd

class HistoryCommand(Command):
    """Command to view calculation history."""
    
    def execute(self):
        """Execute the history command."""
        history_df = HistoryManager.get_history()
        
        if history_df.empty:
            print("No calculation history available.")
            return
        
        # Set display options for better readability
        with pd.option_context('display.max_rows', None, 
                              'display.max_columns', None,
                              'display.width', 120):
            print("\nCalculation History:")
            print(history_df)
