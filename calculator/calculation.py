"""Module for performing calculations using arithmetic operations."""

from decimal import Decimal
from typing import Callable
from calculator.operations import add, subtract, multiply, divide

class Calculation:
    """Represents a mathematical calculation with two operands and an operation."""

    def __init__(self, a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]):
        """Initialize a Calculation with two operands and an operation."""
        self.a = a
        self.b = b
        self.operation = operation

    def perform(self) -> Decimal:
        """Perform the calculation and return the result."""
        return self.operation(self.a, self.b)

    @staticmethod
    def create(a: Decimal, b: Decimal, operation: Callable[[Decimal, Decimal], Decimal]) -> 'Calculation':
        """Static method to create a new Calculation instance."""
        return Calculation(a, b, operation)
    
    def __repr__(self):
        """Return the string representation of the Calculation object."""
        return f"Calculation({self.a}, {self.b}, {self.operation.__name__})"
