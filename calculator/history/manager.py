"""Module for managing calculation history using pandas."""

import os
import pandas as pd
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any, Callable
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide

class HistoryManager:
    """Manages calculation history using pandas DataFrame."""
    
    _history_df = pd.DataFrame(columns=['timestamp', 'a', 'b', 'operation', 'result'])
    _default_file_path = os.path.join(os.getcwd(), 'calculation_history.csv')
    
    # Operation name to function mapping
    _operation_map = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    
    @classmethod
    def add_calculation(cls, calculation: Calculation) -> None:
        """Add a calculation to the history DataFrame."""
        new_row = {
            'timestamp': datetime.now(),
            'a': float(calculation.a),  # Convert Decimal to float for pandas
            'b': float(calculation.b),
            'operation': calculation.operation.__name__,
            'result': float(calculation.perform())
        }
        
        # Create a new DataFrame with the new row
        new_df = pd.DataFrame([new_row])
        
        # If the history DataFrame is empty, just use the new DataFrame
        if cls._history_df.empty:
            cls._history_df = new_df
        else:
            # Otherwise concatenate, ensuring dtypes are preserved
            cls._history_df = pd.concat([cls._history_df, new_df], ignore_index=True)
    
    @classmethod
    def get_history(cls) -> pd.DataFrame:
        """Get the entire history as a pandas DataFrame."""
        return cls._history_df
    
    @classmethod
    def clear_history(cls) -> None:
        """Clear the history DataFrame."""
        cls._history_df = pd.DataFrame(columns=['timestamp', 'a', 'b', 'operation', 'result'])
    
    @classmethod
    def save_history(cls, file_path: Optional[str] = None) -> str:
        """Save the history to a CSV file.
        
        Args:
            file_path: Path to save the file. If None, uses default path.
            
        Returns:
            The path where the file was saved.
        """
        path = file_path or cls._default_file_path
        cls._history_df.to_csv(path, index=False)
        return path
    
    @classmethod
    def load_history(cls, file_path: Optional[str] = None) -> bool:
        """Load history from a CSV file.
        
        Args:
            file_path: Path to load the file from. If None, uses default path.
            
        Returns:
            True if successful, False otherwise.
        """
        path = file_path or cls._default_file_path
        
        if not os.path.exists(path):
            return False
            
        try:
            cls._history_df = pd.read_csv(path)
            # Convert timestamp strings back to datetime objects
            cls._history_df['timestamp'] = pd.to_datetime(cls._history_df['timestamp'])
            return True
        except Exception:
            return False
    
    @classmethod
    def delete_history_file(cls, file_path: Optional[str] = None) -> bool:
        """Delete the history file.
        
        Args:
            file_path: Path to the file to delete. If None, uses default path.
            
        Returns:
            True if successful, False otherwise.
        """
        path = file_path or cls._default_file_path
        
        if not os.path.exists(path):
            return False
            
        try:
            os.remove(path)
            return True
        except Exception:
            return False
    
    @classmethod
    def get_latest(cls) -> Optional[Dict[str, Any]]:
        """Get the latest calculation.
        
        Returns:
            Dictionary with calculation details or None if history is empty.
        """
        if cls._history_df.empty:
            return None
        
        latest = cls._history_df.iloc[-1].to_dict()
        return latest
    
    @classmethod
    def find_by_operation(cls, operation_name: str) -> pd.DataFrame:
        """Find calculations by operation name.
        
        Args:
            operation_name: Name of the operation to filter by.
            
        Returns:
            DataFrame with filtered calculations.
        """
        return cls._history_df[cls._history_df['operation'] == operation_name]
    
    @classmethod
    def to_calculations(cls) -> List[Calculation]:
        """Convert the history DataFrame to a list of Calculation objects.
        
        Returns:
            List of Calculation objects.
        """
        calculations = []
        
        for _, row in cls._history_df.iterrows():
            operation_func = cls._operation_map.get(row['operation'])
            if operation_func:
                calc = Calculation(
                    Decimal(str(row['a'])),
                    Decimal(str(row['b'])),
                    operation_func
                )
                calculations.append(calc)
                
        return calculations
