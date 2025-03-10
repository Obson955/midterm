from calculator.app.commands import Command
from decimal import Decimal, InvalidOperation

class CalculatorCommand(Command):
    def __init__(self, operation):
        self.operation = operation

    def execute(self):
        try:
            a = Decimal(input("Enter the first number: "))
            b = Decimal(input("Enter the second number: "))
            result = self.operation(a, b)
            print(f"Result: {result}")
        except InvalidOperation:
            print("Invalid input. Please enter valid numbers.")
        except ZeroDivisionError:
            print("Error: Division by zero.")

