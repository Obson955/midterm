"""Tests for the advanced plugin commands."""

import os
import pandas as pd
from decimal import Decimal
import pytest
from datetime import datetime, timedelta
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide
from calculator.history.manager import HistoryManager
from calculator.app.plugins.statistics import StatisticsCommand
from calculator.app.plugins.export_excel import ExportExcelCommand
from calculator.app.plugins.filter_history import FilterHistoryCommand


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

    # Create sample calculations
    calculations = [
        Calculation(Decimal('10'), Decimal('5'), add),
        Calculation(Decimal('20'), Decimal('10'), subtract),
        Calculation(Decimal('5'), Decimal('5'), multiply),
        Calculation(Decimal('100'), Decimal('4'), divide),
        Calculation(Decimal('30'), Decimal('15'), add),
    ]

    # Add calculations to history
    for calc in calculations:
        HistoryManager.add_calculation(calc)

    yield
    HistoryManager.clear_history()


@pytest.fixture
def temp_excel_file():
    """Fixture to manage a temporary Excel file."""
    test_file = "test_export_command.xlsx"
    yield test_file
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)


@pytest.mark.usefixtures("populate_history")
def test_statistics_command(capsys):
    """Test the StatisticsCommand."""
    # Create and execute the command
    command = StatisticsCommand()
    command.execute()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Verify the output contains expected statistics
    assert "Statistics for Calculation History" in output
    assert "Total calculations:" in output
    assert "Average result:" in output
    assert "Minimum result:" in output
    assert "Maximum result:" in output
    assert "Operation Breakdown" in output
    assert "add:" in output
    assert "subtract:" in output
    assert "multiply:" in output
    assert "divide:" in output


@pytest.mark.usefixtures("populate_history")
def test_export_excel_command(temp_excel_file, monkeypatch, capsys):
    """Test the ExportExcelCommand."""
    # Mock the input function to return the test file path
    monkeypatch.setattr('builtins.input', lambda _: temp_excel_file)

    # Create and execute the command
    command = ExportExcelCommand()
    command.execute()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Print the output for debugging
    print("\n==== CAPTURED OUTPUT ====")
    print(output)
    print("========================")

    # Verify the output indicates successful export
    assert "Exporting calculation history to Excel" in output, f"Expected 'Exporting calculation history to Excel' in output but got: {output}"
    assert "History exported successfully" in output, f"Expected 'History exported successfully' in output but got: {output}"
    assert temp_excel_file in output, f"Expected '{temp_excel_file}' in output but got: {output}"

    # Verify the file exists and has the correct content
    assert os.path.exists(temp_excel_file)
    df = pd.read_excel(temp_excel_file)
    assert len(df) == 5
    assert 'timestamp' in df.columns
    assert 'a' in df.columns
    assert 'b' in df.columns
    assert 'operation' in df.columns
    assert 'result' in df.columns


@pytest.mark.usefixtures("populate_history")
def test_filter_history_command_by_operation(monkeypatch, capsys):
    """Test the FilterHistoryCommand filtering by operation."""
    # Mock the input function to simulate user selecting operation filter
    inputs = iter(["1", "add", ""])  # Select operation filter, filter for 'add', then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # Create and execute the command
    command = FilterHistoryCommand()
    command.execute()

    # Capture the output
    captured = capsys.readouterr()
    output = captured.out

    # Verify the output shows filtered results
    assert "Filter Calculation History" in output
    assert "Filtered History" in output
    assert "add" in output
    assert "2 results found" in output or "2 calculations found" in output


@pytest.mark.usefixtures("populate_history")
def test_filter_history_command_by_result_range(monkeypatch, capsys):
    """Test the FilterHistoryCommand filtering by result range."""
    # Mock the input function to simulate user selecting result range filter
    inputs = iter(["2", "20", "30", ""])  # Select result range filter, min=20, max=30, then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    # Create and execute the command
    command = FilterHistoryCommand()
    command.execute()
    
    # Capture the output
    captured = capsys.readouterr()
    output = captured.out
    
    # Verify the output shows filtered results
    assert "Filter Calculation History" in output
    assert "Filtered History" in output
    assert "Results between 20 and 30" in output


@pytest.mark.usefixtures("populate_history")
def test_filter_history_command_by_date_range(monkeypatch, capsys):
    """Test the FilterHistoryCommand filtering by date range."""
    # Get today's date in the format expected by the command
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Mock the input function to simulate user selecting date range filter
    inputs = iter(["3", yesterday, today, ""])  # Select date range filter, from yesterday to today, then exit
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    # Create and execute the command
    command = FilterHistoryCommand()
    command.execute()
    
    # Capture the output
    captured = capsys.readouterr()
    output = captured.out
    
    # Verify the output shows filtered results
    assert "Filter Calculation History" in output
    assert "Filtered History" in output
    assert "Date range" in output
