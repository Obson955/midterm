"""Tests for the history management command plugins."""

import os
from decimal import Decimal
from io import StringIO
from unittest.mock import patch
import pytest
from calculator import Calculator
from calculator.history import HistoryManager
from calculator.app.plugins.history import HistoryCommand
from calculator.app.plugins.save_history import SaveHistoryCommand
from calculator.app.plugins.load_history import LoadHistoryCommand
from calculator.app.plugins.clear_history import ClearHistoryCommand
from calculator.app.plugins.delete_history import DeleteHistoryCommand


@pytest.fixture
def clear_history():
    """Fixture to clear history before and after each test."""
    HistoryManager.clear_history()
    yield
    HistoryManager.clear_history()


@pytest.fixture
def setup_sample_calculations():
    """Fixture to add sample calculations to history."""
    HistoryManager.clear_history()
    Calculator.add(Decimal('5'), Decimal('2'))
    Calculator.subtract(Decimal('10'), Decimal('4'))
    Calculator.multiply(Decimal('3'), Decimal('6'))
    yield
    HistoryManager.clear_history()


@pytest.fixture
def create_test_history_file():
    """Fixture to manage test history file."""
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_history.csv")
    
    # Create an empty file
    with open(test_file, 'w') as f:
        f.write("")
        
    yield test_file
    
    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)


@pytest.mark.usefixtures("clear_history")
def test_history_command_empty():
    """Test history command with empty history."""
    with patch('sys.stdout', new=StringIO()) as fake_output:
        HistoryCommand().execute()
        output = fake_output.getvalue()
        assert "No calculation history available" in output


@pytest.mark.usefixtures("setup_sample_calculations")
def test_history_command_with_data():
    """Test history command with data."""
    with patch('sys.stdout', new=StringIO()) as fake_output:
        HistoryCommand().execute()
        output = fake_output.getvalue()
        assert "Calculation History" in output
        assert "add" in output
        assert "subtract" in output
        assert "multiply" in output


@pytest.mark.usefixtures("setup_sample_calculations")
def test_save_history_command():
    """Test save history command."""
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_save_history.csv")
    
    try:
        with patch('builtins.input', return_value=test_file):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                SaveHistoryCommand().execute()
                output = fake_output.getvalue()
                assert "History saved successfully" in output

        # Verify file exists
        assert os.path.exists(test_file)
    finally:
        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_history_command():
    """Test load history command."""
    # Setup
    HistoryManager.clear_history()
    
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_load_history.csv")

    try:
        # First save some history
        Calculator.add(Decimal('5'), Decimal('2'))
        Calculator.subtract(Decimal('10'), Decimal('4'))
        Calculator.multiply(Decimal('3'), Decimal('6'))
        HistoryManager.save_history(test_file)

        # Clear history
        HistoryManager.clear_history()

        # Load history
        with patch('builtins.input', return_value=test_file):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                LoadHistoryCommand().execute()
                output = fake_output.getvalue()
                assert "History loaded successfully" in output

        # Verify history is loaded
        history_df = HistoryManager.get_history()
        assert len(history_df) == 3
        assert 'add' in history_df['operation'].tolist()
        assert 'subtract' in history_df['operation'].tolist()
        assert 'multiply' in history_df['operation'].tolist()

    finally:
        # Clean up
        HistoryManager.clear_history()
        if os.path.exists(test_file):
            os.remove(test_file)


def test_load_history_command_nonexistent_file():
    """Test load history command with nonexistent file."""
    with patch('builtins.input', return_value="nonexistent_file.csv"):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            LoadHistoryCommand().execute()
            output = fake_output.getvalue()
            assert "Error loading history" in output


@pytest.mark.usefixtures("setup_sample_calculations")
def test_clear_history_command():
    """Test clear history command."""
    # Verify history has data
    assert len(HistoryManager.get_history()) == 3

    # Clear history with confirmation
    with patch('builtins.input', return_value="y"):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            ClearHistoryCommand().execute()
            output = fake_output.getvalue()
            assert "History cleared successfully" in output

    # Verify history is empty
    assert len(HistoryManager.get_history()) == 0


@pytest.mark.usefixtures("setup_sample_calculations")
def test_clear_history_command_cancel():
    """Test canceling clear history command."""
    # Verify history has data
    assert len(HistoryManager.get_history()) == 3

    # Cancel clear history
    with patch('builtins.input', return_value="n"):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            ClearHistoryCommand().execute()
            output = fake_output.getvalue()
            assert "Operation cancelled" in output

    # Verify history still has data
    assert len(HistoryManager.get_history()) == 3


def test_delete_history_file_command():
    """Test delete history file command."""
    # Setup
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_delete_history.csv")

    try:
        # First save some history
        HistoryManager.clear_history()
        Calculator.add(Decimal('5'), Decimal('2'))
        Calculator.subtract(Decimal('10'), Decimal('4'))
        Calculator.multiply(Decimal('3'), Decimal('6'))
        HistoryManager.save_history(test_file)

        # Verify file exists
        assert os.path.exists(test_file)

        # Delete file with confirmation
        with patch('builtins.input', side_effect=[test_file, "y"]):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                DeleteHistoryCommand().execute()
                output = fake_output.getvalue()
                assert "History file deleted" in output

        # Verify file is deleted
        assert not os.path.exists(test_file)

    finally:
        # Cleanup in case test fails
        HistoryManager.clear_history()
        if os.path.exists(test_file):
            os.remove(test_file)


def test_delete_history_file_command_cancel():
    """Test canceling delete history file command."""
    # Setup
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_delete_cancel.csv")

    try:
        # First save some history
        HistoryManager.clear_history()
        Calculator.add(Decimal('5'), Decimal('2'))
        Calculator.subtract(Decimal('10'), Decimal('4'))
        Calculator.multiply(Decimal('3'), Decimal('6'))
        HistoryManager.save_history(test_file)

        # Verify file exists
        assert os.path.exists(test_file)

        # Cancel delete file
        with patch('builtins.input', side_effect=[test_file, "n"]):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                DeleteHistoryCommand().execute()
                output = fake_output.getvalue()
                assert "Operation canceled" in output

        # Verify file still exists
        assert os.path.exists(test_file)

    finally:
        # Cleanup
        HistoryManager.clear_history()
        if os.path.exists(test_file):
            os.remove(test_file)


def test_delete_history_file_command_nonexistent_file():
    """Test delete history file command with nonexistent file."""
    with patch('builtins.input', side_effect=["nonexistent_file.csv", "y"]):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            DeleteHistoryCommand().execute()
            output = fake_output.getvalue()
            assert "Error: Could not delete history file" in output
