"""Tests for the advanced features of the HistoryManager class."""

import os
import pandas as pd
from decimal import Decimal
import pytest
from datetime import datetime, timedelta
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.history.manager import HistoryManager


@pytest.fixture
def clear_history():
    """Fixture to clear history before and after each test."""
    HistoryManager.clear_history()
    yield
    HistoryManager.clear_history()


@pytest.fixture
def populate_history():
    """Fixture to populate history with sample data."""
    # Clear any existing history
    HistoryManager.clear_history()
    
    # Create sample calculations with different timestamps
    now = datetime.now()
    
    # Add calculations with specific timestamps for testing date filters
    calculations = [
        (Calculation(Decimal('10'), Decimal('5'), add), now - timedelta(days=5)),
        (Calculation(Decimal('20'), Decimal('10'), subtract), now - timedelta(days=4)),
        (Calculation(Decimal('5'), Decimal('5'), multiply), now - timedelta(days=3)),
        (Calculation(Decimal('100'), Decimal('4'), divide), now - timedelta(days=2)),
        (Calculation(Decimal('30'), Decimal('15'), add), now - timedelta(days=1)),
        (Calculation(Decimal('50'), Decimal('25'), subtract), now),
    ]
    
    # Manually add each calculation with its timestamp
    for calc, timestamp in calculations:
        result = calc.perform()
        new_row = {
            'timestamp': timestamp,
            'a': float(calc.a),
            'b': float(calc.b),
            'operation': calc.operation.__name__,
            'result': float(result)
        }
        new_df = pd.DataFrame([new_row])
        
        if HistoryManager._history_df.empty:
            HistoryManager._history_df = new_df
        else:
            HistoryManager._history_df = pd.concat([HistoryManager._history_df, new_df], ignore_index=True)
    
    yield
    HistoryManager.clear_history()


@pytest.mark.usefixtures("populate_history")
def test_get_statistics():
    """Test getting statistics from history."""
    stats = HistoryManager.get_statistics()
    
    # Check overall statistics
    assert 'overall' in stats
    assert stats['overall']['count'] == 6
    assert 'mean' in stats['overall']
    assert 'min' in stats['overall']
    assert 'max' in stats['overall']
    
    # Check operation-specific statistics
    assert 'add' in stats
    assert stats['add']['count'] == 2
    assert stats['add']['mean'] == 25.0  # (15 + 45) / 2
    
    assert 'subtract' in stats
    assert stats['subtract']['count'] == 2
    assert stats['subtract']['mean'] == 17.5  # (10 + 25) / 2
    
    assert 'multiply' in stats
    assert stats['multiply']['count'] == 1
    assert stats['multiply']['mean'] == 25.0
    
    assert 'divide' in stats
    assert stats['divide']['count'] == 1
    assert stats['divide']['mean'] == 25.0


@pytest.mark.usefixtures("populate_history")
def test_filter_by_date_range():
    """Test filtering history by date range."""
    now = datetime.now()
    
    # Test filtering for the last 2 days
    start_date = now - timedelta(days=2)
    filtered = HistoryManager.filter_by_date_range(start_date)
    
    assert len(filtered) == 2  # Should include the last 2 calculations
    
    # Test with both start and end date
    start_date = now - timedelta(days=4)
    end_date = now - timedelta(days=2)
    filtered = HistoryManager.filter_by_date_range(start_date, end_date)
    
    assert len(filtered) == 3  # Should include calculations from 4, 3, and 2 days ago


@pytest.mark.usefixtures("populate_history")
def test_filter_by_result_range():
    """Test filtering history by result range."""
    # Test filtering for results between 20 and 30
    filtered = HistoryManager.filter_by_result_range(20, 30)
    
    assert len(filtered) == 3  # Should include calculations with results 25, 25, 25
    
    # Test with only min_result
    filtered = HistoryManager.filter_by_result_range(min_result=20)
    
    assert len(filtered) == 4  # Should include calculations with results >= 20
    
    # Test with only max_result
    filtered = HistoryManager.filter_by_result_range(max_result=20)
    
    assert len(filtered) == 2  # Should include calculations with results <= 20


@pytest.mark.usefixtures("populate_history")
def test_get_operations_summary():
    """Test getting operations summary."""
    summary = HistoryManager.get_operations_summary()
    
    assert len(summary) == 4  # Should have 4 operations
    assert summary['add'] == 2
    assert summary['subtract'] == 2
    assert summary['multiply'] == 1
    assert summary['divide'] == 1


@pytest.mark.usefixtures("populate_history")
def test_export_to_excel():
    """Test exporting history to Excel."""
    excel_file = "test_export.xlsx"
    
    try:
        # Export to Excel
        path = HistoryManager.export_to_excel(excel_file)
        
        # Verify file exists
        assert os.path.exists(path)
        
        # Verify file can be read as Excel
        df = pd.read_excel(path)
        assert len(df) == 6
        assert 'timestamp' in df.columns
        assert 'a' in df.columns
        assert 'b' in df.columns
        assert 'operation' in df.columns
        assert 'result' in df.columns
    finally:
        # Clean up
        if os.path.exists(excel_file):
            os.remove(excel_file)


@pytest.mark.usefixtures("populate_history")
def test_get_result_distribution():
    """Test getting result distribution."""
    distribution = HistoryManager.get_result_distribution(bins=3)
    
    # Check that we have a distribution with 3 bins
    assert len(distribution) == 3
    
    # Check that the distribution values sum to the total number of calculations
    assert sum(distribution.values) == 6


@pytest.mark.usefixtures("populate_history")
def test_get_operation_trends():
    """Test getting operation trends over time."""
    trends = HistoryManager.get_operation_trends()
    
    # Check that we have trends for each operation
    assert 'add' in trends
    assert 'subtract' in trends
    assert 'multiply' in trends
    assert 'divide' in trends
    
    # Check that each trend has the correct number of data points
    assert len(trends['add']) == 2
    assert len(trends['subtract']) == 2
    assert len(trends['multiply']) == 1
    assert len(trends['divide']) == 1


@pytest.mark.usefixtures("clear_history")
def test_data_directory_path():
    """Test that the HistoryManager uses the data directory for file operations."""
    # Add a calculation to ensure history has data
    calc = Calculation(Decimal('10'), Decimal('5'), add)
    HistoryManager.add_calculation(calc)
    
    # Save history to default location
    path = HistoryManager.save_history()
    
    # Verify path is in the data directory
    assert 'data' in path
    assert 'calculation_history.csv' in path
    
    # Verify file exists
    assert os.path.exists(path)
    
    # Clean up
    if os.path.exists(path):
        os.remove(path)
