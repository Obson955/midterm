from decimal import Decimal
from calculator.calculation import Calculation
from calculator.calculations import Calculations
from calculator.operations import add, subtract, multiply, divide
from calculator.history import HistoryManager

class Calculator:
    @staticmethod
    def _perform_operation(a: Decimal, b: Decimal, operation) -> Decimal:
        """Perform a calculation and add it to history."""
        calculation = Calculation.create(a, b, operation)
        Calculations.add_calculation(calculation)
        # Also add to pandas-based history manager
        HistoryManager.add_calculation(calculation)
        return calculation.perform()

    @staticmethod
    def add(a: Decimal, b: Decimal) -> Decimal:
        """Add two numbers and store the result in history."""
        return Calculator._perform_operation(a, b, add)

    @staticmethod
    def subtract(a: Decimal, b: Decimal) -> Decimal:
        """Subtract two numbers and store the result in history."""
        return Calculator._perform_operation(a, b, subtract)

    @staticmethod
    def multiply(a: Decimal, b: Decimal) -> Decimal:
        """Multiply two numbers and store the result in history."""
        return Calculator._perform_operation(a, b, multiply)

    @staticmethod
    def divide(a: Decimal, b: Decimal) -> Decimal:
        """Divide two numbers and store the result in history."""
        return Calculator._perform_operation(a, b, divide)