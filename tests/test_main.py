"""Test suite for the calculate_and_print function.

This module contains tests for performing arithmetic operations and handling errors.
"""

import pytest
from main import calculate_and_print  # Ensure this import matches your project structure

# Parameterize the test function to cover different operations and scenarios, including errors
@pytest.mark.parametrize("a_string, b_string, operation_string, expected_string", [
    ("5", "3", 'add',
     "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract',
     "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply',
     "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide',
     "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide',
     "An error occurred: Cannot divide by zero"),
    ("9", "3", 'unknown',
     "Unknown operation: unknown"),
    ("a", "3", 'add',
     "Invalid number input: a or 3 is not a valid number."),
    ("5", "b", 'subtract',
     "Invalid number input: 5 or b is not a valid number."),
    ("-5", "3", 'add',
     "The result of -5 add 3 is equal to -2"),
    ("3", "5", 'subtract',
     "The result of 3 subtract 5 is equal to -2"),
    ("10", "0", 'multiply',
     "The result of 10 multiply 0 is equal to 0"),
    ("10", "4", 'divide',
     "The result of 10 divide 4 is equal to 2.5"),
    ("@", "3", 'add',
     "Invalid number input: @ or 3 is not a valid number.")
])
def test_calculate_and_print(a_string, b_string, operation_string, expected_string, capsys):
    """Test the calculate_and_print function for various operations and error scenarios."""
    calculate_and_print(a_string, b_string, operation_string)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_string
