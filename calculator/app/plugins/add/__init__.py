from calculator.app.commands import Command
from calculator import Calculator
from decimal import Decimal, InvalidOperation

class AddCommand(Command):
    def execute(self):
        try:
            a = Decimal(input("Enter the first number: "))
            b = Decimal(input("Enter the second number: "))
            result = Calculator.add(a, b)
            print(f"Result: {result}")
        except InvalidOperation:
            print("Invalid input. Please enter valid numbers.")
        except ZeroDivisionError:
            print("Error: Division by zero.")