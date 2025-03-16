from calculator.app.commands import Command
from calculator.history.manager import HistoryManager
import pandas as pd
from calculator.logging_config import get_logger

logger = get_logger(__name__)

class StatisticsCommand(Command):
    def execute(self):
        try:
            history_manager = HistoryManager()
            stats = history_manager.get_statistics()
            
            if not stats:
                print("No calculation history available for statistics.")
                logger.info("Statistics command executed but no history was available")
                return
            
            print("\n===== Calculation Statistics =====")
            
            # Overall statistics
            print("\nOverall Statistics:")
            overall = stats.get('overall', {})
            print(f"  Total calculations: {overall.get('count', 0)}")
            print(f"  Average result: {overall.get('mean_result', 0):.4f}")
            print(f"  Minimum result: {overall.get('min_result', 0):.4f}")
            print(f"  Maximum result: {overall.get('max_result', 0):.4f}")
            print(f"  Standard deviation: {overall.get('std_result', 0):.4f}")
            
            # Statistics by operation
            print("\nStatistics by Operation:")
            for op_name, op_stats in stats.items():
                if op_name != 'overall':
                    print(f"\n  {op_name.capitalize()}:")
                    print(f"    Count: {op_stats.get('count', 0)}")
                    print(f"    Average result: {op_stats.get('mean_result', 0):.4f}")
                    print(f"    Minimum result: {op_stats.get('min_result', 0):.4f}")
                    print(f"    Maximum result: {op_stats.get('max_result', 0):.4f}")
                    print(f"    Standard deviation: {op_stats.get('std_result', 0):.4f}")
            
            # Operation frequency
            print("\nOperation Frequency:")
            freq = history_manager.get_operation_frequency()
            for op, count in freq.items():
                print(f"  {op.capitalize()}: {count}")
                
            logger.info("Statistics command executed successfully")
        except Exception as e:
            print(f"Error generating statistics: {e}")
            logger.error(f"Error in statistics command: {e}", exc_info=True)
