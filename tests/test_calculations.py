"""Unit tests for the Calculations class."""

from decimal import Decimal
import pytest

from calculator.calculations import Calculations
from calculator.calculation import Calculation
from calculator.operations import add

@pytest.fixture(autouse=True)
def setup_method():
    """Fixture to clear calculation history before each test."""
    Calculations.clear_history()
    yield
    Calculations.clear_history()

def test_add_calculation():
    """Test adding a calculation to the history."""
    calc = Calculation(Decimal('1.0'), Decimal('2.0'), add)
    Calculations.add_calculation(calc)
    assert len(Calculations.get_history()) == 1

def test_clear_history():
    """Test clearing the calculation history."""
    calc = Calculation(Decimal('1.0'), Decimal('2.0'), add)
    Calculations.add_calculation(calc)
    Calculations.clear_history()
    assert len(Calculations.get_history()) == 0

def test_get_latest():
    """Test retrieving the latest calculation from history."""
    calc1 = Calculation(Decimal('1.0'), Decimal('2.0'), add)
    calc2 = Calculation(Decimal('3.0'), Decimal('4.0'), add)
    Calculations.add_calculation(calc1)
    Calculations.add_calculation(calc2)
    latest = Calculations.get_latest()
    assert latest is calc2

def test_get_latest_with_empty_history():
    """Test getting the latest calculation when the history is empty."""
    latest = Calculations.get_latest()
    assert latest is None, "Expected None for latest calculation with empty history"

def test_find_by_operation():
    """Test finding calculations by operation."""
    calc1 = Calculation(Decimal('1.0'), Decimal('2.0'), add)
    Calculations.add_calculation(calc1)
    add_operations = Calculations.find_by_operation('add')
    assert len(add_operations) == 1, "Should find one calculation with 'add' operation"
    # Test for non-existent operation
    nonexistent_operations = Calculations.find_by_operation('multiply')
    assert len(nonexistent_operations) == 0, "Should find no calculations with 'multiply' operation"

def test_add_calculation_with_zero():
    """Test adding a calculation with zero."""
    calc = Calculation(Decimal('0'), Decimal('0'), add)
    Calculations.add_calculation(calc)
    assert Calculations.get_latest() == calc, "Latest calculation should be with zero values"
