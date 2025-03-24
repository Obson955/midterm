# Calculator Application Documentation

This document provides a detailed explanation of the design patterns, environment variables, logging, and exception handling approaches used in the calculator application.

## Design Patterns

### 1. Singleton Pattern

The Singleton pattern ensures that a class has only one instance and provides a global point of access to it.

**Implementation:**
- Found in `HistoryManager` class in `calculator/history/manager.py`
- Found in `LoggingConfig` class in `calculator/logging_config.py`

```python
# Example from HistoryManager in calculator/history/manager.py
def __new__(cls):
    """Implement singleton pattern."""
    if cls._instance is None:
        cls._instance = super(HistoryManager, cls).__new__(cls)
        # Ensure data directory exists
        cls._data_dir.mkdir(exist_ok=True)
        logger.info(f"HistoryManager singleton instance created, using data directory: {cls._data_dir}")
    return cls._instance
```

The Singleton pattern ensures that we have only one instance of the `HistoryManager` and `LoggingConfig` classes throughout the application, providing consistent access to calculation history and logging configuration.

### 2. Command Pattern

The Command pattern encapsulates a request as an object, allowing parameterization of clients with different requests, queuing of requests, and logging of the requests.

**Implementation:**
- Found in `Command` abstract class in `calculator/app/commands/__init__.py`
- Found in `CommandHandler` class in `calculator/app/commands/__init__.py`
- Various command implementations in `calculator/app/plugins/` directory

```python
# Example from calculator/app/commands/__init__.py
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name: str, command: Command):
        self.commands[command_name] = command

    def execute_command(self, command_name: str):
        try:
            self.commands[command_name].execute()
        except KeyError:
            print(f"No such command: {command_name}")
```

The Command pattern allows the calculator application to encapsulate each operation (add, subtract, etc.) as a command object, making it easy to extend the application with new commands without modifying existing code.

### 3. Facade Pattern

The Facade pattern provides a simplified interface to a complex subsystem.

**Implementation:**
- Found in `PandasFacade` class in `calculator/history/facade.py`

```python
# Example from calculator/history/facade.py
class PandasFacade:
    """Facade for Pandas operations to simplify data manipulation."""
    
    @staticmethod
    def create_dataframe(data: List[Dict[str, Any]] = None, columns: List[str] = None) -> pd.DataFrame:
        """Create a new DataFrame."""
        try:
            if data:
                df = pd.DataFrame(data, columns=columns)
            else:
                df = pd.DataFrame(columns=columns) if columns else pd.DataFrame()
            logger.debug(f"Created new DataFrame with shape {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Error creating DataFrame: {e}")
            raise
```

The Facade pattern simplifies the interaction with the pandas library by providing a clean, high-level interface that hides the complexity of pandas operations, making the code more maintainable and easier to use.

## Environment Variables

The calculator application uses environment variables to configure various aspects of its behavior, providing flexibility without requiring code changes.

**Implementation:**
- Found in `logging_config.py`
- Found in `manager.py`

```python
# Example from calculator/logging_config.py
# Load environment variables from .env file
load_dotenv()

# Get log level from environment variable or default to INFO
log_level_name = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO').upper()
log_level = getattr(logging, log_level_name, logging.INFO)

# Get log destination from environment variable or default to file
log_dest = os.environ.get('CALCULATOR_LOG_DEST', 'file').lower()
```

```python
# Example from calculator/history/manager.py
# Set default file path to data directory from environment variable
_data_dir = pathlib.Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).joinpath(
    os.environ.get('CALCULATOR_DATA_DIR', 'data')
)
_default_file_path = str(_data_dir.joinpath(
    os.environ.get('CALCULATOR_HISTORY_FILE', 'calculation_history.csv')
))
```

The application uses the following environment variables:
- `CALCULATOR_LOG_LEVEL`: Controls the logging level (INFO, DEBUG, WARNING, ERROR)
- `CALCULATOR_LOG_DEST`: Specifies where logs should be written (file, rotating_file, console)
- `CALCULATOR_LOG_FILE`: Custom log file path
- `CALCULATOR_LOG_MAX_BYTES`: Maximum size of log file before rotation
- `CALCULATOR_LOG_BACKUP_COUNT`: Number of backup log files to keep
- `CALCULATOR_DATA_DIR`: Directory for storing data files
- `CALCULATOR_HISTORY_FILE`: Name of the history CSV file

These environment variables allow for flexible configuration without code changes, following the principle of separating configuration from code.

## Logging

The calculator application implements a comprehensive logging system to track application behavior, errors, and important events.

**Implementation:**
- Found in `logging_config.py`
- Used throughout the application

```python
# Example from calculator/logging_config.py
class LoggingConfig:
    """Singleton class for configuring and managing application logging."""
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super(LoggingConfig, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance
    
    def _configure(self):
        """Configure the logging system based on environment variables."""
        # Get log level from environment variable or default to INFO
        log_level_name = os.environ.get('CALCULATOR_LOG_LEVEL', 'INFO').upper()
        log_level = getattr(logging, log_level_name, logging.INFO)
        
        # Get log destination from environment variable or default to file
        log_dest = os.environ.get('CALCULATOR_LOG_DEST', 'file').lower()
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)
```

```python
# Example usage from main.py
logger = get_logger(__name__)

def calculate_and_print(a, b, operation_name):
    # ...
    logger.info(f"Command-line calculation: {a} {operation_name} {b} = {result(a_decimal, b_decimal)}")
    # ...
    logger.error(f"Unknown operation in command-line mode: {operation_name}")
```

The logging system:
1. Uses a Singleton pattern to ensure consistent logging configuration
2. Configures logging based on environment variables
3. Supports multiple log destinations (file, rotating file, console)
4. Logs important events, errors, and debugging information throughout the application
5. Includes timestamp, logger name, and log level in each log entry

This comprehensive logging system helps with debugging, monitoring, and understanding application behavior.

## Exception Handling

The calculator application uses two main approaches to exception handling: "Look Before You Leap" (LBYL) and "Easier to Ask for Forgiveness than Permission" (EAFP).

### LBYL (Look Before You Leap)

This approach checks conditions before attempting an operation.

**Implementation:**
- Found in `CommandHandler.execute_command` (commented example) in `calculator/app/commands/__init__.py`

```python
# Example from calculator/app/commands/__init__.py
""" Look before you leap (LBYL) - Use when its less likely to work
if command_name in self.commands:
    self.commands[command_name].execute()
else:
    print(f"No such command: {command_name}")
"""
```

LBYL is useful when:
- The operation is unlikely to succeed
- The check is inexpensive
- You want to avoid exceptions for control flow

### EAFP (Easier to Ask for Forgiveness than Permission)

This approach attempts an operation and handles exceptions if they occur.

**Implementation:**
- Found in `CommandHandler.execute_command` in `calculator/app/commands/__init__.py`
- Found throughout the application, especially in file operations

```python
# Example from calculator/app/commands/__init__.py
"""Easier to ask for forgiveness than permission (EAFP) - Use when its going to most likely work"""
try:
    self.commands[command_name].execute()
except KeyError:
    print(f"No such command: {command_name}")
```

```python
# Example from main.py
try:
    a_decimal, b_decimal = map(Decimal, [a, b])
    result = operation_mappings.get(operation_name)
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
except Exception as e:
    print(f"An error occurred: {e}")
    logger.error(f"Unexpected error in command-line mode: {e}", exc_info=True)
```

EAFP is useful when:
- The operation is likely to succeed
- Checking would be more expensive than handling the exception
- Multiple failure conditions need to be handled

The calculator application uses both approaches appropriately based on the context, with EAFP being more prevalent due to Python's idiomatic preference for this style.
