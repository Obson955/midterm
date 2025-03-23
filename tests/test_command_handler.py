"""Tests for the command handler module."""

import pytest
from unittest.mock import patch
from decimal import Decimal
from calculator.app.commands.command_handler import CalculatorCommand
from calculator.operations import add, subtract, multiply, divide


def test_calculator_command_execute_add():
    """Test executing a calculator command with addition."""
    with patch('builtins.input', side_effect=['5', '3']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(add)
        command.execute()
        mock_print.assert_called_with('Result: 8')


def test_calculator_command_execute_subtract():
    """Test executing a calculator command with subtraction."""
    with patch('builtins.input', side_effect=['10', '4']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(subtract)
        command.execute()
        mock_print.assert_called_with('Result: 6')


def test_calculator_command_execute_multiply():
    """Test executing a calculator command with multiplication."""
    with patch('builtins.input', side_effect=['6', '7']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(multiply)
        command.execute()
        mock_print.assert_called_with('Result: 42')


def test_calculator_command_execute_divide():
    """Test executing a calculator command with division."""
    with patch('builtins.input', side_effect=['20', '5']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(divide)
        command.execute()
        mock_print.assert_called_with('Result: 4')


def test_calculator_command_invalid_input():
    """Test executing a calculator command with invalid input."""
    with patch('builtins.input', side_effect=['abc', '5']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(add)
        command.execute()
        mock_print.assert_called_with('Invalid input. Please enter valid numbers.')


def test_calculator_command_division_by_zero():
    """Test executing a calculator command with division by zero."""
    # Create a mock operation that raises ZeroDivisionError
    def mock_divide(a, b):
        raise ZeroDivisionError("Cannot divide by zero")
    
    with patch('builtins.input', side_effect=['10', '0']), patch('builtins.print') as mock_print:
        command = CalculatorCommand(mock_divide)
        command.execute()
        mock_print.assert_called_with('Error: Division by zero.')
