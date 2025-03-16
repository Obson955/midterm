from calculator.app.commands import Command
from calculator.history.manager import HistoryManager
from calculator.logging_config import get_logger
import pandas as pd
from datetime import datetime, timedelta

logger = get_logger(__name__)

class FilterHistoryCommand(Command):
    def execute(self):
        try:
            history_manager = HistoryManager()
            history_df = history_manager.get_history()
            
            if history_df.empty:
                print("No calculation history available to filter.")
                logger.info("Filter history command executed but no history was available")
                return
            
            print("\n===== Filter Calculation History =====")
            print("1. Filter by date range")
            print("2. Filter by result range")
            print("3. Filter by operation type")
            print("0. Cancel")
            
            choice = input("\nEnter your choice (0-3): ").strip()
            
            if choice == '0':
                return
            
            filtered_df = None
            
            if choice == '1':
                # Filter by date range
                print("\nFilter by date range:")
                print("Available date range: ")
                min_date = history_df['timestamp'].min().strftime('%Y-%m-%d')
                max_date = history_df['timestamp'].max().strftime('%Y-%m-%d')
                print(f"From {min_date} to {max_date}")
                
                # Default to last 7 days if available
                default_start = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                default_end = datetime.now().strftime('%Y-%m-%d')
                
                start_date = input(f"Enter start date (YYYY-MM-DD) [default: {default_start}]: ").strip()
                if not start_date:
                    start_date = default_start
                
                end_date = input(f"Enter end date (YYYY-MM-DD) [default: {default_end}]: ").strip()
                if not end_date:
                    end_date = default_end
                
                filtered_df = history_manager.filter_by_date_range(start_date, end_date)
                logger.info(f"Filtered history by date range: {start_date} to {end_date}")
                
            elif choice == '2':
                # Filter by result range
                print("\nFilter by result range:")
                min_result = history_df['result'].min()
                max_result = history_df['result'].max()
                print(f"Available result range: {min_result} to {max_result}")
                
                min_input = input(f"Enter minimum result [default: {min_result}]: ").strip()
                min_value = float(min_input) if min_input else min_result
                
                max_input = input(f"Enter maximum result [default: {max_result}]: ").strip()
                max_value = float(max_input) if max_input else max_result
                
                filtered_df = history_manager.filter_by_result_range(min_value, max_value)
                logger.info(f"Filtered history by result range: {min_value} to {max_value}")
                
            elif choice == '3':
                # Filter by operation type
                print("\nFilter by operation type:")
                operations = history_df['operation'].unique()
                
                for i, op in enumerate(operations, 1):
                    print(f"{i}. {op}")
                
                op_choice = input("Enter operation number: ").strip()
                try:
                    op_index = int(op_choice) - 1
                    if 0 <= op_index < len(operations):
                        operation = operations[op_index]
                        filtered_df = history_manager.find_by_operation(operation)
                        logger.info(f"Filtered history by operation: {operation}")
                    else:
                        print("Invalid operation number.")
                        return
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    return
            
            # Display filtered results
            if filtered_df is not None and not filtered_df.empty:
                print(f"\nFound {len(filtered_df)} matching calculations:")
                
                # Format the DataFrame for display
                display_df = filtered_df.copy()
                display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                display_df = display_df.rename(columns={
                    'timestamp': 'Timestamp',
                    'a': 'First Number',
                    'b': 'Second Number',
                    'operation': 'Operation',
                    'result': 'Result'
                })
                
                # Set display options for better formatting
                with pd.option_context('display.max_rows', 10, 'display.max_columns', None, 'display.width', 120):
                    print(display_df.to_string(index=False))
                
                # If there are more than 10 rows, show a message
                if len(display_df) > 10:
                    print(f"\n(Showing first 10 of {len(display_df)} results)")
            else:
                print("No calculations match the filter criteria.")
                
        except Exception as e:
            print(f"Error filtering history: {e}")
            logger.error(f"Error in filter history command: {e}", exc_info=True)
