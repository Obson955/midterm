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
            
            print("\n===== Statistics for Calculation History =====")
            
            # Overall statistics
            print("\nOverall Statistics:")
            overall = stats.get('overall', {})
            print(f"  Total calculations: {overall.get('count', 0)}")
            print(f"  Average result: {overall.get('mean', 0):.4f}")
            print(f"  Minimum result: {overall.get('min', 0):.4f}")
            print(f"  Maximum result: {overall.get('max', 0):.4f}")
            print(f"  Standard deviation: {overall.get('std', 0):.4f}")
            
            # Statistics by operation
            print("\nStatistics by Operation:")
            for op_name, op_stats in stats.items():
                if op_name != 'overall':
                    print(f"\n  {op_name}:")
                    print(f"    Count: {op_stats.get('count', 0)}")
                    print(f"    Average result: {op_stats.get('mean', 0):.4f}")
                    print(f"    Minimum result: {op_stats.get('min', 0):.4f}")
                    print(f"    Maximum result: {op_stats.get('max', 0):.4f}")
                    print(f"    Standard deviation: {op_stats.get('std', 0):.4f}")
            
            # Operation Breakdown
            print("\nOperation Breakdown:")
            for op_name, op_stats in stats.items():
                if op_name != 'overall':
                    print(f"  {op_name}: {op_stats.get('count', 0)}")
                
            logger.info("Statistics command executed successfully")
        except Exception as e:
            print(f"Error generating statistics: {e}")
            logger.error(f"Error in statistics command: {e}", exc_info=True)
