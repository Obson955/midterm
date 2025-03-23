"""Module implementing the Facade pattern for Pandas data operations."""

import os
import pandas as pd
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from calculator.logging_config import get_logger

# Get module logger
logger = get_logger(__name__)

class PandasFacade:
    """Facade for Pandas operations to simplify data manipulation."""
    
    @staticmethod
    def create_dataframe(data: List[Dict[str, Any]] = None, columns: List[str] = None) -> pd.DataFrame:
        """Create a new DataFrame.
        
        Args:
            data: List of dictionaries with data.
            columns: List of column names.
            
        Returns:
            New DataFrame.
        """
        try:
            if data:
                df = pd.DataFrame(data, columns=columns)
            else:
                df = pd.DataFrame(columns=columns) if columns else pd.DataFrame()
            logger.debug(f"Created new DataFrame with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error creating DataFrame: {e}")
            raise
    
    @staticmethod
    def read_csv(file_path: str, **kwargs) -> pd.DataFrame:
        """Read data from CSV file.
        
        Args:
            file_path: Path to CSV file.
            **kwargs: Additional arguments for pd.read_csv.
            
        Returns:
            DataFrame with data from CSV.
        """
        try:
            if not os.path.exists(file_path):
                logger.warning(f"CSV file not found: {file_path}")
                return pd.DataFrame()
                
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Read CSV file {file_path} with {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error reading CSV file {file_path}: {e}")
            raise
    
    @staticmethod
    def write_csv(df: pd.DataFrame, file_path: str, **kwargs) -> str:
        """Write DataFrame to CSV file.
        
        Args:
            df: DataFrame to write.
            file_path: Path to save CSV file.
            **kwargs: Additional arguments for df.to_csv.
            
        Returns:
            Path where file was saved.
        """
        try:
            df.to_csv(file_path, **kwargs)
            logger.info(f"Wrote DataFrame with {len(df)} rows to CSV file {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error writing CSV file {file_path}: {e}")
            raise
    
    @staticmethod
    def filter_by_value(df: pd.DataFrame, column: str, value: Any) -> pd.DataFrame:
        """Filter DataFrame by column value.
        
        Args:
            df: DataFrame to filter.
            column: Column name to filter on.
            value: Value to filter by.
            
        Returns:
            Filtered DataFrame.
        """
        try:
            if column not in df.columns:
                logger.warning(f"Column '{column}' not found in DataFrame")
                return pd.DataFrame(columns=df.columns)
                
            filtered = df[df[column] == value]
            logger.debug(f"Filtered DataFrame by {column}={value}, got {len(filtered)} rows")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering DataFrame: {e}")
            raise
    
    @staticmethod
    def filter_by_range(df: pd.DataFrame, column: str, min_value: Any, max_value: Any) -> pd.DataFrame:
        """Filter DataFrame by column value range.
        
        Args:
            df: DataFrame to filter.
            column: Column name to filter on.
            min_value: Minimum value (inclusive).
            max_value: Maximum value (inclusive).
            
        Returns:
            Filtered DataFrame.
        """
        try:
            if column not in df.columns:
                logger.warning(f"Column '{column}' not found in DataFrame")
                return pd.DataFrame(columns=df.columns)
                
            filtered = df[(df[column] >= min_value) & (df[column] <= max_value)]
            logger.debug(f"Filtered DataFrame by {min_value} <= {column} <= {max_value}, got {len(filtered)} rows")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering DataFrame by range: {e}")
            raise
    
    @staticmethod
    def filter_by_date_range(df: pd.DataFrame, date_column: str, 
                            start_date: Union[str, datetime], 
                            end_date: Union[str, datetime]) -> pd.DataFrame:
        """Filter DataFrame by date range.
        
        Args:
            df: DataFrame to filter.
            date_column: Date column name.
            start_date: Start date (inclusive).
            end_date: End date (inclusive).
            
        Returns:
            Filtered DataFrame.
        """
        try:
            if date_column not in df.columns:
                logger.warning(f"Date column '{date_column}' not found in DataFrame")
                return pd.DataFrame(columns=df.columns)
            
            # Ensure date column is datetime type
            if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
                df[date_column] = pd.to_datetime(df[date_column])
            
            # Convert string dates to datetime if needed
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date)
            if isinstance(end_date, str):
                end_date = pd.to_datetime(end_date)
            
            filtered = df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]
            logger.debug(f"Filtered DataFrame by date range {start_date} to {end_date}, got {len(filtered)} rows")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering DataFrame by date range: {e}")
            raise
    
    @staticmethod
    def get_statistics(df: pd.DataFrame, columns: List[str] = None) -> Dict[str, Dict[str, float]]:
        """Get statistical information about DataFrame columns.
        
        Args:
            df: DataFrame to analyze.
            columns: List of columns to include. If None, uses all numeric columns.
            
        Returns:
            Dictionary with statistics for each column.
        """
        try:
            if df.empty:
                logger.debug("Attempted to get statistics but DataFrame is empty")
                return {}
            
            # If no columns specified, use all numeric columns
            if not columns:
                columns = df.select_dtypes(include=['number']).columns.tolist()
            
            stats = {}
            for column in columns:
                if column in df.columns:
                    col_stats = {
                        'count': df[column].count(),
                        'mean': df[column].mean() if pd.api.types.is_numeric_dtype(df[column]) else None,
                        'min': df[column].min() if pd.api.types.is_numeric_dtype(df[column]) else None,
                        'max': df[column].max() if pd.api.types.is_numeric_dtype(df[column]) else None,
                        'std': df[column].std() if pd.api.types.is_numeric_dtype(df[column]) else None
                    }
                    stats[column] = {k: v for k, v in col_stats.items() if v is not None}
            
            logger.debug(f"Generated statistics for {len(stats)} columns")
            return stats
        except Exception as e:
            logger.error(f"Error generating statistics: {e}")
            raise
    
    @staticmethod
    def pivot_table(df: pd.DataFrame, index: str, values: str, 
                   aggfunc: Union[str, List[str]] = 'mean') -> pd.DataFrame:
        """Create a pivot table from DataFrame.
        
        Args:
            df: DataFrame to pivot.
            index: Column to use as index.
            values: Column to aggregate.
            aggfunc: Aggregation function(s) to use.
            
        Returns:
            Pivot table DataFrame.
        """
        try:
            if df.empty:
                logger.debug("Attempted to create pivot table but DataFrame is empty")
                return pd.DataFrame()
            
            if index not in df.columns or values not in df.columns:
                missing = []
                if index not in df.columns:
                    missing.append(f"index '{index}'")
                if values not in df.columns:
                    missing.append(f"values '{values}'")
                logger.warning(f"Columns not found in DataFrame: {', '.join(missing)}")
                return pd.DataFrame()
            
            pivot = pd.pivot_table(df, index=index, values=values, aggfunc=aggfunc)
            logger.debug(f"Created pivot table with shape {pivot.shape}")
            return pivot
        except Exception as e:
            logger.error(f"Error creating pivot table: {e}")
            raise
    
    @staticmethod
    def generate_chart(df: pd.DataFrame, chart_type: str, x: str = None, y: str = None, 
                      title: str = "Chart", figsize: Tuple[int, int] = (10, 6)) -> str:
        """Generate chart from DataFrame and return as base64 encoded string.
        
        Args:
            df: DataFrame with data.
            chart_type: Type of chart ('bar', 'line', 'pie', 'hist').
            x: Column for x-axis.
            y: Column for y-axis.
            title: Chart title.
            figsize: Figure size (width, height) in inches.
            
        Returns:
            Base64 encoded PNG image.
        """
        try:
            if df.empty:
                logger.debug("Attempted to generate chart but DataFrame is empty")
                return ""
            
            plt.figure(figsize=figsize)
            
            if chart_type == 'bar':
                if x and y and x in df.columns and y in df.columns:
                    df.plot(kind='bar', x=x, y=y, title=title)
                else:
                    df.plot(kind='bar', title=title)
            elif chart_type == 'line':
                if x and y and x in df.columns and y in df.columns:
                    df.plot(kind='line', x=x, y=y, title=title)
                else:
                    df.plot(kind='line', title=title)
            elif chart_type == 'pie' and x in df.columns:
                df[x].value_counts().plot(kind='pie', title=title, autopct='%1.1f%%')
            elif chart_type == 'hist' and x in df.columns:
                df[x].plot(kind='hist', title=title, bins=10)
            else:
                logger.warning(f"Invalid chart type or missing required columns")
                return ""
            
            plt.tight_layout()
            
            # Save chart to bytes buffer
            buffer = BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            
            # Encode as base64
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close()
            
            logger.debug(f"Generated {chart_type} chart")
            return image_base64
        except Exception as e:
            logger.error(f"Error generating chart: {e}")
            plt.close()
            raise
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, file_path: str, sheet_name: str = 'Sheet1',
                       include_stats: bool = False) -> str:
        """Export DataFrame to Excel file.
        
        Args:
            df: DataFrame to export.
            file_path: Path to save Excel file.
            sheet_name: Name for the main sheet.
            include_stats: Whether to include statistics sheet.
            
        Returns:
            Path where file was saved.
        """
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Write main data sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Add statistics sheet if requested
                if include_stats and not df.empty:
                    stats = PandasFacade.get_statistics(df)
                    stats_df = pd.DataFrame()
                    
                    for col_name, col_stats in stats.items():
                        col_df = pd.DataFrame([col_stats], index=[col_name])
                        stats_df = pd.concat([stats_df, col_df])
                    
                    stats_df.to_excel(writer, sheet_name='Statistics')
            
            logger.info(f"Exported DataFrame with {len(df)} rows to Excel file {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error exporting to Excel {file_path}: {e}")
            raise
    
    @staticmethod
    def merge_dataframes(left_df: pd.DataFrame, right_df: pd.DataFrame, 
                        on: Union[str, List[str]], how: str = 'inner') -> pd.DataFrame:
        """Merge two DataFrames.
        
        Args:
            left_df: Left DataFrame.
            right_df: Right DataFrame.
            on: Column(s) to join on.
            how: Type of merge ('inner', 'outer', 'left', 'right').
            
        Returns:
            Merged DataFrame.
        """
        try:
            merged = pd.merge(left_df, right_df, on=on, how=how)
            logger.debug(f"Merged DataFrames with shapes {left_df.shape} and {right_df.shape} into {merged.shape}")
            return merged
        except Exception as e:
            logger.error(f"Error merging DataFrames: {e}")
            raise
    
    @staticmethod
    def group_by(df: pd.DataFrame, by: Union[str, List[str]], 
                agg_dict: Dict[str, Union[str, List[str]]]) -> pd.DataFrame:
        """Group DataFrame by columns and aggregate.
        
        Args:
            df: DataFrame to group.
            by: Column(s) to group by.
            agg_dict: Dictionary mapping columns to aggregation functions.
            
        Returns:
            Grouped DataFrame.
        """
        try:
            if df.empty:
                logger.debug("Attempted to group empty DataFrame")
                return pd.DataFrame()
                
            grouped = df.groupby(by).agg(agg_dict).reset_index()
            logger.debug(f"Grouped DataFrame by {by}, result shape {grouped.shape}")
            return grouped
        except Exception as e:
            logger.error(f"Error grouping DataFrame: {e}")
            raise
