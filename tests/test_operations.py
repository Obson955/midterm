"""Test suite for calculator operations."""

from decimal import Decimal
import pytest

from calculator.operations import add, subtract, multiply, divide

def test_add():
    """Test addition of two decimal numbers."""
    assert add(Decimal('1.1'), Decimal('2.2')) == Decimal('3.3')

def test_subtract():
    """Test subtraction of two decimal numbers."""
    assert subtract(Decimal('5.5'), Decimal('2.2')) == Decimal('3.3')

def test_multiply():
    """Test multiplication of two decimal numbers."""
    assert multiply(Decimal('2.0'), Decimal('3.5')) == Decimal('7.0')

def test_divide():
    """Test division of two decimal numbers."""
    assert divide(Decimal('7.0'), Decimal('2.0')) == Decimal('3.5')

def test_divide_by_zero():
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(Decimal('1.0'), Decimal('0.0'))

def test_add_with_negative_numbers():
    """Test addition with negative numbers."""
    assert add(Decimal('-1.1'), Decimal('2.2')) == Decimal('1.1')

def test_subtract_with_negative_numbers():
    """Test subtraction resulting in negative numbers."""
    assert subtract(Decimal('2.2'), Decimal('5.5')) == Decimal('-3.3')

def test_multiply_with_zero():
    """Test multiplication with zero."""
    assert multiply(Decimal('2.0'), Decimal('0.0')) == Decimal('0.0')
    assert multiply(Decimal('0.0'), Decimal('3.5')) == Decimal('0.0')

def test_divide_with_one():
    """Test division by one."""
    assert divide(Decimal('7.0'), Decimal('1.0')) == Decimal('7.0')

def test_large_number_operations():
    """Test operations with large numbers."""
    large_number = Decimal('1e10')
    assert add(large_number, large_number) == Decimal('2e10')
    assert subtract(large_number, large_number) == Decimal('0')
    assert multiply(large_number, Decimal('2')) == Decimal('2e10')
    assert divide(large_number, Decimal('2')) == Decimal('5e9')
