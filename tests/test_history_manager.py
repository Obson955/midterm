"""Tests for the HistoryManager class."""

import os
from decimal import Decimal
import pytest
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply
from calculator.history import HistoryManager
from unittest.mock import patch


@pytest.fixture
def clear_history():
    """Fixture to clear history before and after each test."""
    HistoryManager.clear_history()
    yield
    HistoryManager.clear_history()


@pytest.fixture
def create_sample_calculations():
    """Fixture to create sample calculations."""
    calc1 = Calculation(Decimal('5'), Decimal('2'), add)
    calc2 = Calculation(Decimal('10'), Decimal('5'), subtract)
    calc3 = Calculation(Decimal('4'), Decimal('3'), multiply)
    return [calc1, calc2, calc3]


@pytest.fixture
def create_history_file():
    """Fixture to manage test history file."""
    test_file = "test_history.csv"
    yield test_file
    # Clean up after test
    if os.path.exists(test_file):
        os.remove(test_file)


@pytest.mark.usefixtures("clear_history")
def test_add_calculation():
    """Test adding a calculation to the history."""
    # Create a sample calculation
    calc = Calculation(Decimal('5'), Decimal('2'), add)

    # Add a calculation
    HistoryManager.add_calculation(calc)

    # Check that the history has one entry
    history_df = HistoryManager.get_history()
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'add'
    assert history_df.iloc[0]['a'] == 5.0
    assert history_df.iloc[0]['b'] == 2.0
    assert history_df.iloc[0]['result'] == 7.0


@pytest.mark.usefixtures("clear_history")
def test_add_multiple_calculations():
    """Test adding multiple calculations to the history."""
    # Create sample calculations
    calcs = [
        Calculation(Decimal('5'), Decimal('2'), add),
        Calculation(Decimal('10'), Decimal('5'), subtract),
        Calculation(Decimal('4'), Decimal('3'), multiply)
    ]

    # Add multiple calculations
    for calc in calcs:
        HistoryManager.add_calculation(calc)

    # Check that the history has the correct number of entries
    history_df = HistoryManager.get_history()
    assert len(history_df) == 3

    # Check operations are recorded correctly
    operations = history_df['operation'].tolist()
    assert operations == ['add', 'subtract', 'multiply']

    # Check results are calculated correctly
    results = history_df['result'].tolist()
    assert results == [7.0, 5.0, 12.0]


@pytest.mark.usefixtures("clear_history")
def test_clear_history():
    """Test clearing the history."""
    # Create and add calculations
    calcs = [
        Calculation(Decimal('5'), Decimal('2'), add),
        Calculation(Decimal('10'), Decimal('5'), subtract),
        Calculation(Decimal('4'), Decimal('3'), multiply)
    ]

    for calc in calcs:
        HistoryManager.add_calculation(calc)

    # Verify history has entries
    assert len(HistoryManager.get_history()) == 3

    # Clear history
    HistoryManager.clear_history()

    # Verify history is empty
    assert len(HistoryManager.get_history()) == 0
    assert HistoryManager.get_history().empty


@pytest.mark.usefixtures("clear_history")
def test_save_and_load_history():
    """Test saving and loading history."""
    # Setup
    HistoryManager.clear_history()
    
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_save_load.csv")
    
    try:
        # Add some calculations to history
        calc1 = Calculation(Decimal('5'), Decimal('2'), add)
        calc2 = Calculation(Decimal('10'), Decimal('4'), subtract)
        
        HistoryManager.add_calculation(calc1)
        HistoryManager.add_calculation(calc2)
        
        # Save history
        saved_path = HistoryManager.save_history(test_file)
        assert saved_path == test_file
        assert os.path.exists(test_file)
        
        # Clear history
        HistoryManager.clear_history()
        assert len(HistoryManager.get_history()) == 0
        
        # Load history
        assert HistoryManager.load_history(test_file)
        
        # Check history is loaded
        history = HistoryManager.get_history()
        assert len(history) == 2
        assert 'add' in history['operation'].values
        assert 'subtract' in history['operation'].values
    finally:
        # Clean up
        HistoryManager.clear_history()
        if os.path.exists(test_file):
            os.remove(test_file)


@pytest.mark.usefixtures("clear_history")
def test_load_nonexistent_file():
    """Test loading from a nonexistent file."""
    success = HistoryManager.load_history("nonexistent_file.csv")
    assert not success
    assert HistoryManager.get_history().empty


@pytest.mark.usefixtures("clear_history")
def test_delete_history_file():
    """Test deleting history file."""
    # Setup
    HistoryManager.clear_history()
    
    # Create a test file in the data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)
    test_file = os.path.join(data_dir, "test_delete.csv")
    
    try:
        # Add some calculations to history
        calc1 = Calculation(Decimal('5'), Decimal('2'), add)
        calc2 = Calculation(Decimal('10'), Decimal('4'), subtract)
        
        HistoryManager.add_calculation(calc1)
        HistoryManager.add_calculation(calc2)
        
        # Save history
        HistoryManager.save_history(test_file)
        assert os.path.exists(test_file)
        
        # Test deletion directly without the confirmation prompt
        # This is a direct test of the underlying method
        os.remove(test_file)
        assert not os.path.exists(test_file)
        
        # For testing the confirmation logic, we need to recreate the file
        HistoryManager.save_history(test_file)
        assert os.path.exists(test_file)
        
        # Now test the full method with mocked input
        with patch('builtins.input', return_value='y'):
            result = HistoryManager.delete_history_file(test_file)
            assert result
            assert not os.path.exists(test_file)
    finally:
        # Clean up
        HistoryManager.clear_history()
        if os.path.exists(test_file):
            os.remove(test_file)


@pytest.mark.usefixtures("clear_history")
def test_delete_nonexistent_file():
    """Test deleting a nonexistent file."""
    success = HistoryManager.delete_history_file("nonexistent_file.csv")
    assert not success


@pytest.mark.usefixtures("clear_history")
def test_get_latest():
    """Test getting the latest calculation."""
    # Create and add calculations
    calcs = [
        Calculation(Decimal('5'), Decimal('2'), add),
        Calculation(Decimal('10'), Decimal('5'), subtract),
        Calculation(Decimal('4'), Decimal('3'), multiply)
    ]

    for calc in calcs:
        HistoryManager.add_calculation(calc)

    # Get latest
    latest = HistoryManager.get_latest()
    assert latest is not None
    assert latest['operation'] == 'multiply'
    assert latest['a'] == 4.0
    assert latest['b'] == 3.0
    assert latest['result'] == 12.0


@pytest.mark.usefixtures("clear_history")
def test_get_latest_empty_history():
    """Test getting latest with empty history."""
    latest = HistoryManager.get_latest()
    assert latest is None


@pytest.mark.usefixtures("clear_history")
def test_find_by_operation():
    """Test finding calculations by operation."""
    # Create and add calculations
    calcs = [
        Calculation(Decimal('5'), Decimal('2'), add),
        Calculation(Decimal('10'), Decimal('5'), subtract),
        Calculation(Decimal('4'), Decimal('3'), multiply)
    ]

    for calc in calcs:
        HistoryManager.add_calculation(calc)

    # Find by operation
    add_operations = HistoryManager.find_by_operation('add')
    assert len(add_operations) == 1
    assert add_operations.iloc[0]['a'] == 5.0
    assert add_operations.iloc[0]['b'] == 2.0

    # Find nonexistent operation
    divide_operations = HistoryManager.find_by_operation('divide')
    assert len(divide_operations) == 0


@pytest.mark.usefixtures("clear_history")
def test_to_calculations():
    """Test converting history to Calculation objects."""
    # Create and add calculations
    calcs = [
        Calculation(Decimal('5'), Decimal('2'), add),
        Calculation(Decimal('10'), Decimal('5'), subtract),
        Calculation(Decimal('4'), Decimal('3'), multiply)
    ]

    for calc in calcs:
        HistoryManager.add_calculation(calc)

    # Convert to calculations
    calculations = HistoryManager.to_calculations()
    assert len(calculations) == 3

    # Verify calculations
    assert calculations[0].operation.__name__ == 'add'
    assert calculations[1].operation.__name__ == 'subtract'
    assert calculations[2].operation.__name__ == 'multiply'

    # Verify calculation performs correctly
    assert calculations[0].perform() == Decimal('7')
