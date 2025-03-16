"""Module for managing calculation history using pandas."""

import os
import pandas as pd
import numpy as np
import pathlib
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, Dict, Any, Callable, Union, Tuple, Union, Tuple
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.logging_config import get_logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get module logger
logger = get_logger(__name__)
from calculator.logging_config import get_logger
import pathlib

# Get module logger
logger = get_logger(__name__)

class HistoryManager:
    """Manages calculation history using pandas DataFrame."""
    
    _history_df = pd.DataFrame(columns=['timestamp', 'a', 'b', 'operation', 'result'])
    # Set default file path to data directory from environment variable
    _data_dir = pathlib.Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).joinpath(
        os.environ.get('CALCULATOR_DATA_DIR', 'data')
    )
    _default_file_path = str(_data_dir.joinpath(
        os.environ.get('CALCULATOR_HISTORY_FILE', 'calculation_history.csv')
    ))
    _instance = None  # For singleton pattern
    
    # Operation name to function mapping
    _operation_map = {
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(HistoryManager, cls).__new__(cls)
            # Ensure data directory exists
            cls._data_dir.mkdir(exist_ok=True)
            logger.info(f"HistoryManager singleton instance created, using data directory: {cls._data_dir}")
        return cls._instance
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(HistoryManager, cls).__new__(cls)
            # Ensure data directory exists
            cls._data_dir.mkdir(exist_ok=True)
            logger.info(f"HistoryManager singleton instance created, using data directory: {cls._data_dir}")
        return cls._instance
    
    @classmethod
    def add_calculation(cls, calculation: Calculation) -> None:
        """Add a calculation to the history DataFrame."""
        try:
            result = calculation.perform()
            new_row = {
                'timestamp': datetime.now(),
                'a': float(calculation.a),  # Convert Decimal to float for pandas
                'b': float(calculation.b),
                'operation': calculation.operation.__name__,
                'result': float(result)
            }
            
            # Create a new DataFrame with the new row
            new_df = pd.DataFrame([new_row])
            
            # If the history DataFrame is empty, just use the new DataFrame
            if cls._history_df.empty:
                cls._history_df = new_df
            else:
                # Otherwise concatenate, ensuring dtypes are preserved
                cls._history_df = pd.concat([cls._history_df, new_df], ignore_index=True)
            
            logger.info(f"Added calculation to history: {calculation.a} {calculation.operation.__name__} {calculation.b} = {result}")
        except Exception as e:
            logger.error(f"Error adding calculation to history: {e}")
            raise
        try:
            result = calculation.perform()
            new_row = {
                'timestamp': datetime.now(),
                'a': float(calculation.a),  # Convert Decimal to float for pandas
                'b': float(calculation.b),
                'operation': calculation.operation.__name__,
                'result': float(result)
            }
            
            # Create a new DataFrame with the new row
            new_df = pd.DataFrame([new_row])
            
            # If the history DataFrame is empty, just use the new DataFrame
            if cls._history_df.empty:
                cls._history_df = new_df
            else:
                # Otherwise concatenate, ensuring dtypes are preserved
                cls._history_df = pd.concat([cls._history_df, new_df], ignore_index=True)
            
            logger.info(f"Added calculation to history: {calculation.a} {calculation.operation.__name__} {calculation.b} = {result}")
        except Exception as e:
            logger.error(f"Error adding calculation to history: {e}")
            raise
    
    @classmethod
    def get_history(cls) -> pd.DataFrame:
        """Get the entire history as a pandas DataFrame."""
        logger.debug("Retrieved calculation history")
        logger.debug("Retrieved calculation history")
        return cls._history_df
    
    @classmethod
    def clear_history(cls) -> None:
        """Clear the history DataFrame."""
        cls._history_df = pd.DataFrame(columns=['timestamp', 'a', 'b', 'operation', 'result'])
        logger.info("Calculation history cleared")
        logger.info("Calculation history cleared")
    
    @classmethod
    def save_history(cls, file_path: Optional[str] = None) -> str:
        """Save the history to a CSV file.
        
        Args:
            file_path: Path to save the file. If None, uses default path.
            
        Returns:
            The path where the file was saved.
        """
        path = file_path or cls._default_file_path
        try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            try:
            # Ensure parent directory exists
            os.makedirs(os.path.dirname(path), exist_ok=True)
            cls._history_df.to_csv(path, index=False)
            logger.info(f"Calculation history saved to {path}")
                logger.info(f"Calculation history saved to {path}")
            return path
        except Exception as e:
            logger.error(f"Error saving history to {path}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error saving history to {path}: {e}")
            raise
    
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
            logger.warning(f"History file not found: {path}")
            logger.warning(f"History file not found: {path}")
            return False
            
        try:
            cls._history_df = pd.read_csv(path)
            # Convert timestamp strings back to datetime objects
            cls._history_df['timestamp'] = pd.to_datetime(cls._history_df['timestamp'])
            logger.info(f"Calculation history loaded from {path}")
            logger.info(f"Calculation history loaded from {path}")
            return True
        except Exception as e:
            logger.error(f"Error loading history from {path}: {e}")
        except Exception as e:
            logger.error(f"Error loading history from {path}: {e}")
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
            logger.warning(f"History file not found for deletion: {path}")
            return False
            
        try:
            os.remove(path)
            logger.info(f"History file deleted: {path}")
            logger.info(f"History file deleted: {path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting history file {path}: {e}")
        except Exception as e:
            logger.error(f"Error deleting history file {path}: {e}")
            return False
    
    @classmethod
    def get_latest(cls) -> Optional[Dict[str, Any]]:
        """Get the latest calculation.
        
        Returns:
            Dictionary with calculation details or None if history is empty.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get latest calculation but history is empty")
            logger.debug("Attempted to get latest calculation but history is empty")
            return None
        
        latest = cls._history_df.iloc[-1].to_dict()
        logger.debug(f"Retrieved latest calculation: {latest}")
        logger.debug(f"Retrieved latest calculation: {latest}")
        return latest
    
    @classmethod
    def find_by_operation(cls, operation_name: str) -> pd.DataFrame:
        """Find calculations by operation name.
        
        Args:
            operation_name: Name of the operation to filter by.
            
        Returns:
            DataFrame with filtered calculations.
        """
        result = cls._history_df[cls._history_df['operation'] == operation_name]
        logger.debug(f"Found {len(result)} calculations with operation '{operation_name}'")
        return result
        result = cls._history_df[cls._history_df['operation'] == operation_name]
        logger.debug(f"Found {len(result)} calculations with operation '{operation_name}'")
        return result
    
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
                
        logger.debug(f"Converted {len(calculations)} history records to Calculation objects")
        logger.debug(f"Converted {len(calculations)} history records to Calculation objects")
        return calculations
    
    # Advanced Pandas data handling methods
    
    @classmethod
    def get_statistics(cls) -> Dict[str, Dict[str, float]]:
        """Get statistical information about calculations.
        
        Returns:
            Dictionary with statistics for each operation and overall.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get statistics but history is empty")
            return {}
        
        stats = {}
        
        # Overall statistics
        stats['overall'] = {
            'count': len(cls._history_df),
            'mean_result': cls._history_df['result'].mean(),
            'min_result': cls._history_df['result'].min(),
            'max_result': cls._history_df['result'].max(),
            'std_result': cls._history_df['result'].std()
        }
        
        # Statistics by operation
        for operation in cls._history_df['operation'].unique():
            op_df = cls._history_df[cls._history_df['operation'] == operation]
            stats[operation] = {
                'count': len(op_df),
                'mean_result': op_df['result'].mean(),
                'min_result': op_df['result'].min(),
                'max_result': op_df['result'].max(),
                'std_result': op_df['result'].std()
            }
        
        logger.info("Generated calculation statistics")
        return stats
    
    @classmethod
    def filter_by_date_range(cls, start_date: Union[str, datetime], end_date: Union[str, datetime]) -> pd.DataFrame:
        """Filter calculations by date range.
        
        Args:
            start_date: Start date (inclusive) as string or datetime.
            end_date: End date (inclusive) as string or datetime.
            
        Returns:
            DataFrame with filtered calculations.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to filter by date range but history is empty")
            return pd.DataFrame(columns=cls._history_df.columns)
        
        # Convert string dates to datetime if needed
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # Filter by date range
        filtered = cls._history_df[
            (cls._history_df['timestamp'] >= start_date) & 
            (cls._history_df['timestamp'] <= end_date)
        ]
        
        logger.debug(f"Filtered {len(filtered)} calculations between {start_date} and {end_date}")
        return filtered
    
    @classmethod
    def filter_by_result_range(cls, min_result: float, max_result: float) -> pd.DataFrame:
        """Filter calculations by result range.
        
        Args:
            min_result: Minimum result value (inclusive).
            max_result: Maximum result value (inclusive).
            
        Returns:
            DataFrame with filtered calculations.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to filter by result range but history is empty")
            return pd.DataFrame(columns=cls._history_df.columns)
        
        filtered = cls._history_df[
            (cls._history_df['result'] >= min_result) & 
            (cls._history_df['result'] <= max_result)
        ]
        
        logger.debug(f"Filtered {len(filtered)} calculations with result between {min_result} and {max_result}")
        return filtered
    
    @classmethod
    def export_to_excel(cls, file_path: str) -> str:
        """Export history to Excel file.
        
        Args:
            file_path: Path to save the Excel file.
            
        Returns:
            The path where the file was saved.
        """
        try:
            # Create a writer object
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Write the main history sheet
                cls._history_df.to_excel(writer, sheet_name='History', index=False)
                
                # Write statistics sheet if history is not empty
                if not cls._history_df.empty:
                    stats = cls.get_statistics()
                    stats_df = pd.DataFrame()
                    
                    for op_name, op_stats in stats.items():
                        op_df = pd.DataFrame([op_stats], index=[op_name])
                        stats_df = pd.concat([stats_df, op_df])
                    
                    stats_df.to_excel(writer, sheet_name='Statistics')
                    
                    # Create a pivot table sheet
                    pivot = pd.pivot_table(
                        cls._history_df,
                        values='result',
                        index='operation',
                        aggfunc=['count', 'mean', 'min', 'max', 'std']
                    )
                    pivot.to_excel(writer, sheet_name='Pivot')
            
            logger.info(f"Calculation history exported to Excel: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error exporting history to Excel {file_path}: {e}")
            raise
    
    @classmethod
    def get_operation_frequency(cls) -> pd.Series:
        """Get frequency of each operation.
        
        Returns:
            Series with operation counts.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get operation frequency but history is empty")
            return pd.Series(dtype=int)
        
        freq = cls._history_df['operation'].value_counts()
        logger.debug(f"Retrieved operation frequency: {freq.to_dict()}")
        return freq
    
    @classmethod
    def get_result_distribution(cls, bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Get distribution of calculation results.
        
        Args:
            bins: Number of bins for the histogram.
            
        Returns:
            Tuple of (bin_edges, histogram_values).
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get result distribution but history is empty")
            return np.array([]), np.array([])
        
        hist, bin_edges = np.histogram(cls._history_df['result'], bins=bins)
        logger.debug(f"Generated result distribution with {bins} bins")
        return bin_edges, hist
    
    # Advanced Pandas data handling methods
    
    @classmethod
    def get_statistics(cls) -> Dict[str, Dict[str, float]]:
        """Get statistical information about calculations.
        
        Returns:
            Dictionary with statistics for each operation and overall.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get statistics but history is empty")
            return {}
        
        stats = {}
        
        # Overall statistics
        stats['overall'] = {
            'count': len(cls._history_df),
            'mean_result': cls._history_df['result'].mean(),
            'min_result': cls._history_df['result'].min(),
            'max_result': cls._history_df['result'].max(),
            'std_result': cls._history_df['result'].std()
        }
        
        # Statistics by operation
        for operation in cls._history_df['operation'].unique():
            op_df = cls._history_df[cls._history_df['operation'] == operation]
            stats[operation] = {
                'count': len(op_df),
                'mean_result': op_df['result'].mean(),
                'min_result': op_df['result'].min(),
                'max_result': op_df['result'].max(),
                'std_result': op_df['result'].std()
            }
        
        logger.info("Generated calculation statistics")
        return stats
    
    @classmethod
    def filter_by_date_range(cls, start_date: Union[str, datetime], end_date: Union[str, datetime]) -> pd.DataFrame:
        """Filter calculations by date range.
        
        Args:
            start_date: Start date (inclusive) as string or datetime.
            end_date: End date (inclusive) as string or datetime.
            
        Returns:
            DataFrame with filtered calculations.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to filter by date range but history is empty")
            return pd.DataFrame(columns=cls._history_df.columns)
        
        # Convert string dates to datetime if needed
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # Filter by date range
        filtered = cls._history_df[
            (cls._history_df['timestamp'] >= start_date) & 
            (cls._history_df['timestamp'] <= end_date)
        ]
        
        logger.debug(f"Filtered {len(filtered)} calculations between {start_date} and {end_date}")
        return filtered
    
    @classmethod
    def filter_by_result_range(cls, min_result: float, max_result: float) -> pd.DataFrame:
        """Filter calculations by result range.
        
        Args:
            min_result: Minimum result value (inclusive).
            max_result: Maximum result value (inclusive).
            
        Returns:
            DataFrame with filtered calculations.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to filter by result range but history is empty")
            return pd.DataFrame(columns=cls._history_df.columns)
        
        filtered = cls._history_df[
            (cls._history_df['result'] >= min_result) & 
            (cls._history_df['result'] <= max_result)
        ]
        
        logger.debug(f"Filtered {len(filtered)} calculations with result between {min_result} and {max_result}")
        return filtered
    
    @classmethod
    def export_to_excel(cls, file_path: str) -> str:
        """Export history to Excel file.
        
        Args:
            file_path: Path to save the Excel file.
            
        Returns:
            The path where the file was saved.
        """
        try:
            # Create a writer object
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Write the main history sheet
                cls._history_df.to_excel(writer, sheet_name='History', index=False)
                
                # Write statistics sheet if history is not empty
                if not cls._history_df.empty:
                    stats = cls.get_statistics()
                    stats_df = pd.DataFrame()
                    
                    for op_name, op_stats in stats.items():
                        op_df = pd.DataFrame([op_stats], index=[op_name])
                        stats_df = pd.concat([stats_df, op_df])
                    
                    stats_df.to_excel(writer, sheet_name='Statistics')
                    
                    # Create a pivot table sheet
                    pivot = pd.pivot_table(
                        cls._history_df,
                        values='result',
                        index='operation',
                        aggfunc=['count', 'mean', 'min', 'max', 'std']
                    )
                    pivot.to_excel(writer, sheet_name='Pivot')
            
            logger.info(f"Calculation history exported to Excel: {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error exporting history to Excel {file_path}: {e}")
            raise
    
    @classmethod
    def get_operation_frequency(cls) -> pd.Series:
        """Get frequency of each operation.
        
        Returns:
            Series with operation counts.
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get operation frequency but history is empty")
            return pd.Series(dtype=int)
        
        freq = cls._history_df['operation'].value_counts()
        logger.debug(f"Retrieved operation frequency: {freq.to_dict()}")
        return freq
    
    @classmethod
    def get_result_distribution(cls, bins: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """Get distribution of calculation results.
        
        Args:
            bins: Number of bins for the histogram.
            
        Returns:
            Tuple of (bin_edges, histogram_values).
        """
        if cls._history_df.empty:
            logger.debug("Attempted to get result distribution but history is empty")
            return np.array([]), np.array([])
        
        hist, bin_edges = np.histogram(cls._history_df['result'], bins=bins)
        logger.debug(f"Generated result distribution with {bins} bins")
        return bin_edges, hist
