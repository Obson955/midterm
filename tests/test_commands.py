"""Unit tests for the Commands."""

#import pytest
from calculator.app import App
from calculator.app.plugins.add import AddCommand
from calculator.app.plugins.subtract import SubtractCommand
from calculator.app.plugins.multiply import MultiplyCommand
from calculator.app.plugins.divide import DivideCommand
from calculator.app.plugins.menu import MenuCommand
#from calculator.app.commands import Command

def test_add_command(capfd, monkeypatch):
    """Test that the AddCommand correctly adds two numbers."""
    inputs = iter(['5', '10'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = AddCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert out == "Result: 15\n", "The AddCommand should print the correct result"

def test_subtract_command(capfd, monkeypatch):
    """Test that the SubtractCommand correctly subtracts two numbers."""
    inputs = iter(['10', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = SubtractCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert out == "Result: 5\n", "The SubtractCommand should print the correct result"

def test_multiply_command(capfd, monkeypatch):
    """Test that the MultiplyCommand correctly multiplies two numbers."""
    inputs = iter(['5', '10'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = MultiplyCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert out == "Result: 50\n", "The MultiplyCommand should print the correct result"

def test_divide_command(capfd, monkeypatch):
    """Test that the DivideCommand correctly divides two numbers."""
    inputs = iter(['10', '5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    command = DivideCommand()
    command.execute()

    out, _ = capfd.readouterr()
    assert out == "Result: 2\n", "The DivideCommand should print the correct result"

def test_menu_command(capfd):
    """Test that the MenuCommand correctly shows the available commands."""
    command = MenuCommand()
    command.execute()

    out, _ = capfd.readouterr()
    expected_output = """Available commands:
1. greet - Greet the user
2. add - Add two numbers
3. subtract - Subtract two numbers
4. multiply - Multiply two numbers
5. divide - Divide two numbers
6. menu - Show this menu
7. exit - Exit the application
8. goodbye - Say goodbye"""

    assert out.strip() == expected_output.strip(), "The MenuCommand should print the correct menu"

def test_app_command_execution(capfd, monkeypatch):
    """Test that the App REPL correctly handles commands and exits."""
    inputs = iter(['add', '5', '10', 'menu', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.start()

    out, _ = capfd.readouterr()
    assert "Result: 15" in out, "The add command should work correctly"
    assert "Available commands:" in out, "The menu command should work correctly"
