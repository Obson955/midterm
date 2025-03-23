import sys
from calculator import Calculator
from decimal import Decimal, InvalidOperation
from calculator.app import App
from calculator.logging_config import get_logger

# Get module logger
logger = get_logger(__name__)

def calculate_and_print(a, b, operation_name):
    operation_mappings = {
        'add': Calculator.add,
        'subtract': Calculator.subtract,
        'multiply': Calculator.multiply,
        'divide': Calculator.divide
    }

    # Unified error handling for decimal conversion
    try:
        a_decimal, b_decimal = map(Decimal, [a, b])
        result = operation_mappings.get(operation_name) # Use get to handle unknown operations
        if result:
            print(f"The result of {a} {operation_name} {b} is equal to {result(a_decimal, b_decimal)}")
            logger.info(f"Command-line calculation: {a} {operation_name} {b} = {result(a_decimal, b_decimal)}")
        else:
            print(f"Unknown operation: {operation_name}")
            logger.error(f"Unknown operation in command-line mode: {operation_name}")
    except InvalidOperation:
        print(f"Invalid number input: {a} or {b} is not a valid number.")
        logger.error(f"Invalid number input in command-line mode: {a} or {b}")
    except ZeroDivisionError:
        print("Error: Division by zero.")
        logger.error("Division by zero in command-line mode")
    except Exception as e: # Catch-all for unexpected errors
        print(f"An error occurred: {e}")
        logger.error(f"Unexpected error in command-line mode: {e}", exc_info=True)

def main():
    """Main entry point for the calculator application.
    
    Supports two modes of operation:
    1. Command line mode: python main.py <number1> <number2> <operation>
    2. Interactive mode: python main.py interactive
    
    If no arguments are provided, defaults to interactive mode.
    """
    logger.info(f"Application started with arguments: {sys.argv[1:]}")
    
    # If no arguments are provided, default to interactive mode
    if len(sys.argv) == 1:
        logger.info("No arguments provided, defaulting to interactive mode")
        app = App()
        app.start()
        return
    
    # Check if running in interactive mode
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'interactive':
        logger.info("Starting in interactive mode")
        app = App()
        app.start()
        return
    
    # Check if running in command-line mode
    if len(sys.argv) == 4:
        logger.info("Starting in command-line mode")
        _, a, b, operation = sys.argv
        calculate_and_print(a, b, operation)
        return
    
    # If we get here, the arguments are invalid
    print("Usage:")
    print("  Interactive mode: python main.py interactive")
    print("  Command line mode: python main.py <number1> <number2> <operation>")
    print("\nAvailable operations: add, subtract, multiply, divide")
    logger.error(f"Invalid command-line arguments: {sys.argv[1:]}")
    sys.exit(1)

if __name__ == '__main__':
    main()