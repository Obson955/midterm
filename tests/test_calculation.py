"""Test suite for the Calculation class."""

from decimal import Decimal
import pytest
from calculator.calculation import Calculation
from calculator.operations import add, subtract, divide, multiply

def test_calculation_add():
    """Test performing an addition calculation."""
    calc = Calculation(Decimal('1.0'), Decimal('2.0'), add)
    assert calc.perform() == Decimal('3.0')

def test_calculation_subtract():
    """Test performing a subtraction calculation."""
    calc = Calculation(Decimal('5.0'), Decimal('3.0'), subtract)
    assert calc.perform() == Decimal('2.0')

def test_calculation_divide_by_zero():
    """Test division by zero."""
    calc = Calculation(Decimal('10.0'), Decimal('0.0'), divide)
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.perform()

def test_calculation_repr():
    """Test the string representation of the Calculation class."""
    calc = Calculation(Decimal('10.0'), Decimal('5.0'), add)
    assert repr(calc) == "Calculation(10.0, 5.0, add)"

def test_calculation_multiply():
    """Test performing a multiplication calculation."""
    calc = Calculation(Decimal('3.0'), Decimal('4.0'), multiply)
    assert calc.perform() == Decimal('12.0')

def test_calculation_create():
    """Test creating a Calculation using the static method."""
    calc = Calculation.create(Decimal('7.0'), Decimal('3.0'), subtract)
    assert isinstance(calc, Calculation)
    assert calc.perform() == Decimal('4.0')

def test_calculation_with_negative_numbers():
    """Test calculations with negative numbers."""
    calc = Calculation(Decimal('-5.0'), Decimal('3.0'), add)
    assert calc.perform() == Decimal('-2.0')

def test_calculation_with_large_numbers():
    """Test calculations with large numbers."""
    large_number = Decimal('1e10')
    calc = Calculation(large_number, large_number, add)
    assert calc.perform() == Decimal('2e10')
