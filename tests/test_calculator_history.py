"""Tests for the integration of Calculator with HistoryManager."""

from decimal import Decimal
import pytest
from calculator import Calculator
from calculator.history import HistoryManager


@pytest.fixture
def clear_history():
    """Fixture to clear history before and after each test."""
    HistoryManager.clear_history()
    yield
    HistoryManager.clear_history()


@pytest.mark.usefixtures("clear_history")
def test_calculator_add_records_history():
    """Test that Calculator.add records the calculation in history."""
    # Perform a calculation
    result = Calculator.add(Decimal('10'), Decimal('5'))

    # Check result
    assert result == Decimal('15')

    # Check history
    history_df = HistoryManager.get_history()
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'add'
    assert history_df.iloc[0]['a'] == 10.0
    assert history_df.iloc[0]['b'] == 5.0
    assert history_df.iloc[0]['result'] == 15.0


@pytest.mark.usefixtures("clear_history")
def test_calculator_subtract_records_history():
    """Test that Calculator.subtract records the calculation in history."""
    # Perform a calculation
    result = Calculator.subtract(Decimal('10'), Decimal('5'))

    # Check result
    assert result == Decimal('5')

    # Check history
    history_df = HistoryManager.get_history()
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'subtract'
    assert history_df.iloc[0]['a'] == 10.0
    assert history_df.iloc[0]['b'] == 5.0
    assert history_df.iloc[0]['result'] == 5.0


@pytest.mark.usefixtures("clear_history")
def test_calculator_multiply_records_history():
    """Test that Calculator.multiply records the calculation in history."""
    # Perform a calculation
    result = Calculator.multiply(Decimal('10'), Decimal('5'))

    # Check result
    assert result == Decimal('50')

    # Check history
    history_df = HistoryManager.get_history()
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'multiply'
    assert history_df.iloc[0]['a'] == 10.0
    assert history_df.iloc[0]['b'] == 5.0
    assert history_df.iloc[0]['result'] == 50.0


@pytest.mark.usefixtures("clear_history")
def test_calculator_divide_records_history():
    """Test that Calculator.divide records the calculation in history."""
    # Perform a calculation
    result = Calculator.divide(Decimal('10'), Decimal('5'))

    # Check result
    assert result == Decimal('2')

    # Check history
    history_df = HistoryManager.get_history()
    assert len(history_df) == 1
    assert history_df.iloc[0]['operation'] == 'divide'
    assert history_df.iloc[0]['a'] == 10.0
    assert history_df.iloc[0]['b'] == 5.0
    assert history_df.iloc[0]['result'] == 2.0


@pytest.mark.usefixtures("clear_history")
def test_multiple_calculations_recorded_in_order():
    """Test that multiple calculations are recorded in order."""
    # Perform multiple calculations
    Calculator.add(Decimal('1'), Decimal('2'))
    Calculator.subtract(Decimal('5'), Decimal('3'))
    Calculator.multiply(Decimal('4'), Decimal('2'))

    # Check history
    history_df = HistoryManager.get_history()
    assert len(history_df) == 3

    # Check operations are recorded in order
    operations = history_df['operation'].tolist()
    assert operations == ['add', 'subtract', 'multiply']

    # Check results are calculated correctly
    results = history_df['result'].tolist()
    assert results == [3.0, 2.0, 8.0]
