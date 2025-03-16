"""Tests for the PandasFacade class."""

import os
import pandas as pd
import numpy as np
import pytest
from calculator.history.facade import PandasFacade


@pytest.fixture
def sample_data():
    """Fixture to create sample data for testing."""
    data = {
        'timestamp': pd.date_range(start='2025-01-01', periods=5),
        'a': [10, 20, 30, 40, 50],
        'b': [5, 10, 15, 20, 25],
        'operation': ['add', 'subtract', 'multiply', 'divide', 'add'],
        'result': [15, 10, 450, 2, 75]
    }
    return data


@pytest.fixture
def sample_dataframe(sample_data):
    """Fixture to create a sample DataFrame for testing."""
    return pd.DataFrame(sample_data)


@pytest.fixture
def temp_csv_file():
    """Fixture to manage a temporary CSV file."""
    test_file = "test_facade.csv"
    yield test_file
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)


def test_create_dataframe():
    """Test creating a DataFrame from data."""
    data = {
        'a': [1, 2, 3],
        'b': [4, 5, 6],
        'c': [7, 8, 9]
    }
    
    df = PandasFacade.create_dataframe(data)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ['a', 'b', 'c']
    assert df['a'].tolist() == [1, 2, 3]
    assert df['b'].tolist() == [4, 5, 6]
    assert df['c'].tolist() == [7, 8, 9]


def test_read_csv(sample_dataframe, temp_csv_file):
    """Test reading a CSV file."""
    # First save the DataFrame to CSV
    sample_dataframe.to_csv(temp_csv_file, index=False)
    
    # Read the CSV using the facade
    df = PandasFacade.read_csv(temp_csv_file)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5
    assert 'timestamp' in df.columns
    assert 'a' in df.columns
    assert 'b' in df.columns
    assert 'operation' in df.columns
    assert 'result' in df.columns


def test_write_csv(sample_dataframe, temp_csv_file):
    """Test writing a DataFrame to CSV."""
    # Write the DataFrame to CSV using the facade
    PandasFacade.write_csv(sample_dataframe, temp_csv_file)
    
    # Verify file exists
    assert os.path.exists(temp_csv_file)
    
    # Read the file to verify contents
    df = pd.read_csv(temp_csv_file)
    assert len(df) == 5
    assert 'a' in df.columns
    assert 'b' in df.columns
    assert 'operation' in df.columns
    assert 'result' in df.columns


def test_filter_by_value(sample_dataframe):
    """Test filtering a DataFrame by value."""
    # Filter for 'add' operations
    filtered = PandasFacade.filter_by_value(sample_dataframe, 'operation', 'add')
    
    assert len(filtered) == 2
    assert filtered['operation'].tolist() == ['add', 'add']
    
    # Filter for results greater than 20
    filtered = PandasFacade.filter_by_value(sample_dataframe, 'result', 20, comparison='>')
    
    assert len(filtered) == 2
    assert filtered['result'].tolist() == [450, 75]


def test_filter_by_date_range(sample_dataframe):
    """Test filtering a DataFrame by date range."""
    # Filter for dates after the second day
    start_date = pd.Timestamp('2025-01-02')
    filtered = PandasFacade.filter_by_date_range(sample_dataframe, 'timestamp', start_date)
    
    assert len(filtered) == 4
    
    # Filter for dates between the second and fourth day
    start_date = pd.Timestamp('2025-01-02')
    end_date = pd.Timestamp('2025-01-04')
    filtered = PandasFacade.filter_by_date_range(sample_dataframe, 'timestamp', start_date, end_date)
    
    assert len(filtered) == 3


def test_get_statistics(sample_dataframe):
    """Test getting statistics from a DataFrame."""
    # Get statistics for the 'result' column
    stats = PandasFacade.get_statistics(sample_dataframe, 'result')
    
    assert 'count' in stats
    assert 'mean' in stats
    assert 'std' in stats
    assert 'min' in stats
    assert 'max' in stats
    
    assert stats['count'] == 5
    assert stats['min'] == 2
    assert stats['max'] == 450


def test_get_group_statistics(sample_dataframe):
    """Test getting grouped statistics from a DataFrame."""
    # Get statistics for 'result' grouped by 'operation'
    grouped_stats = PandasFacade.get_group_statistics(sample_dataframe, 'operation', 'result')
    
    assert 'add' in grouped_stats
    assert 'subtract' in grouped_stats
    assert 'multiply' in grouped_stats
    assert 'divide' in grouped_stats
    
    assert grouped_stats['add']['count'] == 2
    assert grouped_stats['add']['mean'] == 45.0  # (15 + 75) / 2
    assert grouped_stats['subtract']['count'] == 1
    assert grouped_stats['multiply']['count'] == 1
    assert grouped_stats['divide']['count'] == 1


def test_get_value_counts(sample_dataframe):
    """Test getting value counts from a DataFrame."""
    # Get counts of each operation
    counts = PandasFacade.get_value_counts(sample_dataframe, 'operation')
    
    assert counts['add'] == 2
    assert counts['subtract'] == 1
    assert counts['multiply'] == 1
    assert counts['divide'] == 1


def test_export_to_excel(sample_dataframe):
    """Test exporting a DataFrame to Excel."""
    excel_file = "test_facade_excel.xlsx"
    
    try:
        # Export to Excel using the facade
        PandasFacade.export_to_excel(sample_dataframe, excel_file)
        
        # Verify file exists
        assert os.path.exists(excel_file)
        
        # Verify file can be read as Excel
        df = pd.read_excel(excel_file)
        assert len(df) == 5
        assert 'a' in df.columns
        assert 'b' in df.columns
        assert 'operation' in df.columns
        assert 'result' in df.columns
    finally:
        # Clean up
        if os.path.exists(excel_file):
            os.remove(excel_file)


def test_get_histogram_data(sample_dataframe):
    """Test getting histogram data from a DataFrame."""
    # Get histogram data for 'result' column with 3 bins
    hist_data = PandasFacade.get_histogram_data(sample_dataframe, 'result', bins=3)
    
    assert len(hist_data) == 3
    assert isinstance(hist_data, np.ndarray)
    assert sum(hist_data) == 5  # Sum of frequencies should equal number of rows


def test_get_time_series_data(sample_dataframe):
    """Test getting time series data from a DataFrame."""
    # Get time series data for 'result' column
    ts_data = PandasFacade.get_time_series_data(sample_dataframe, 'timestamp', 'result')
    
    assert isinstance(ts_data, pd.Series)
    assert len(ts_data) == 5
    assert ts_data.index.name == 'timestamp'
    assert ts_data.tolist() == [15, 10, 450, 2, 75]
