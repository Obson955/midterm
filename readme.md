# Project Install Instructions

## Calculator Demo

[Watch the demo video here](https://youtu.be/39hkv91oYQg)


## Projects Setup
1. Clone the repository.
2. CD into the project folder.
3. Create and activate the virtual environment (VE).
4. Install the required libraries.
5. Create a `.env` file based on the `.env.example` template.

## Install 

1. Clone the repository
2. Run `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and customize settings as needed

## Environment Configuration

The calculator application uses environment variables for configuration. These can be set in a `.env` file in the project root directory. The following variables are supported:

### Logging Configuration
- `CALCULATOR_LOG_LEVEL`: Sets the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `CALCULATOR_LOG_DEST`: Sets the logging destination (file, console, rotating_file)
- `CALCULATOR_LOG_FILE`: Path for the log file (default: logs/calculator.log)
- `CALCULATOR_LOG_MAX_BYTES`: Maximum size for rotating log files in bytes (default: 1MB)
- `CALCULATOR_LOG_BACKUP_COUNT`: Number of backup log files to keep (default: 3)

### Data Storage Configuration
- `CALCULATOR_DATA_DIR`: Directory for storing data files (default: data)
- `CALCULATOR_HISTORY_FILE`: Filename for calculation history (default: calculation_history.csv)

## Application Modes

The calculator supports two modes of operation:
1. Command line mode: `python main.py <number1> <number2> <operation>` - Performs a single calculation and exits
2. Interactive mode: `python main.py interactive` - Starts the interactive application with a command loop

## Testing 

1. `pytest` - Run all tests
2. `pytest --pylint` - Run tests with pylint checks
3. `pytest --pylint --cov` - Run tests with pylint and coverage reports
4. `pytest --num_records=10` - Run tests with a specific number of test records