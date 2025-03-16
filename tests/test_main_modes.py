"""Tests for the main.py functionality with different operation modes."""

import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from decimal import Decimal
from calculator.calculation import Calculation
from calculator.operations import add, subtract, multiply, divide


@pytest.fixture
def mock_app():
    """Fixture to mock the App class."""
    with patch('calculator.app.App') as mock:
        # Create a mock instance
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_logger():
    """Fixture to mock the logger."""
    with patch('calculator.logging_config.get_logger') as mock:
        mock_logger = MagicMock()
        mock.return_value = mock_logger
        yield mock_logger


def test_command_line_mode(mock_app, mock_logger):
    """Test the command-line mode of operation."""
    # Import main here to avoid module-level patches affecting other tests
    from main import main
    
    # Mock sys.argv
    test_args = ['main.py', '10', '5', 'add']
    with patch.object(sys, 'argv', test_args):
        # Mock the calculate_and_print function
        with patch('main.calculate_and_print') as mock_calc:
            main()
            
            # Verify calculate_and_print was called with correct arguments
            mock_calc.assert_called_once_with('10', '5', 'add')
            
            # Verify App.start() was not called
            mock_app.start.assert_not_called()
            
            # Verify logging
            mock_logger.info.assert_any_call("Application started with arguments: ['10', '5', 'add']")
            mock_logger.info.assert_any_call("Starting in command-line mode")


def test_interactive_mode(mock_app, mock_logger):
    """Test the interactive mode of operation."""
    # Import main here to avoid module-level patches affecting other tests
    from main import main
    
    # Mock sys.argv
    test_args = ['main.py', 'interactive']
    with patch.object(sys, 'argv', test_args):
        main()
        
        # Verify App.start() was called
        mock_app.start.assert_called_once()
        
        # Verify logging
        mock_logger.info.assert_any_call("Application started with arguments: ['interactive']")
        mock_logger.info.assert_any_call("Starting in interactive mode")


def test_default_to_interactive_mode(mock_app, mock_logger):
    """Test that the application defaults to interactive mode when no arguments are provided."""
    # Import main here to avoid module-level patches affecting other tests
    from main import main
    
    # Mock sys.argv
    test_args = ['main.py']
    with patch.object(sys, 'argv', test_args):
        main()
        
        # Verify App.start() was called
        mock_app.start.assert_called_once()
        
        # Verify logging
        mock_logger.info.assert_any_call("Application started with arguments: []")
        mock_logger.info.assert_any_call("No arguments provided, defaulting to interactive mode")


def test_invalid_arguments(mock_app, mock_logger):
    """Test handling of invalid command-line arguments."""
    # Import main here to avoid module-level patches affecting other tests
    from main import main
    
    # Mock sys.argv with invalid number of arguments
    test_args = ['main.py', '10', '5']  # Missing operation
    with patch.object(sys, 'argv', test_args):
        # Mock sys.exit to prevent actual exit
        with patch('sys.exit') as mock_exit:
            main()
            
            # Verify sys.exit was called with exit code 1
            mock_exit.assert_called_once_with(1)
            
            # Verify App.start() was not called
            mock_app.start.assert_not_called()
            
            # Verify error logging
            mock_logger.error.assert_called_once()


def test_calculate_and_print_valid_calculation():
    """Test the calculate_and_print function with valid inputs."""
    # Import calculate_and_print here to avoid module-level patches affecting other tests
    from main import calculate_and_print
    
    # Mock the print function
    with patch('builtins.print') as mock_print:
        # Test with valid inputs
        calculate_and_print('10', '5', 'add')
        
        # Verify print was called with correct result
        mock_print.assert_called_once_with("The result of 10 add 5 is equal to 15")


def test_calculate_and_print_invalid_number():
    """Test the calculate_and_print function with invalid number inputs."""
    # Import calculate_and_print here to avoid module-level patches affecting other tests
    from main import calculate_and_print
    
    # Mock the print function
    with patch('builtins.print') as mock_print:
        # Test with invalid number
        calculate_and_print('abc', '5', 'add')
        
        # Verify print was called with error message
        mock_print.assert_called_once_with("Invalid number input: abc or 5 is not a valid number.")


def test_calculate_and_print_division_by_zero():
    """Test the calculate_and_print function with division by zero."""
    # Import calculate_and_print here to avoid module-level patches affecting other tests
    from main import calculate_and_print
    
    # Mock the print function
    with patch('builtins.print') as mock_print:
        # Test division by zero
        calculate_and_print('10', '0', 'divide')
        
        # Verify print was called with error message
        mock_print.assert_called_once_with("Error: Division by zero.")


def test_calculate_and_print_unknown_operation():
    """Test the calculate_and_print function with an unknown operation."""
    # Import calculate_and_print here to avoid module-level patches affecting other tests
    from main import calculate_and_print
    
    # Mock the print function
    with patch('builtins.print') as mock_print:
        # Test with unknown operation
        calculate_and_print('10', '5', 'unknown')
        
        # Verify print was called with error message
        mock_print.assert_called_once_with("Unknown operation: unknown")
