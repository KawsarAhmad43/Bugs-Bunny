# bug_fixer_agent/logger.py
import logging
import sys
from datetime import datetime

class Logger:
    def __init__(self, name="BugFixerAgent"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create console handler if it doesn't exist
        if not self.logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def get_timestamp(self) -> str:
        """
        Returns current timestamp in a consistent format.
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_bug_processing(self, bug_name: str, status: str, details: str = ""):
        """
        Specialized logging for bug processing events.
        """
        timestamp = self.get_timestamp()
        message = f"[{timestamp}] Bug: {bug_name} | Status: {status}"
        if details:
            message += f" | Details: {details}"
        self.info(message)

    def log_api_call(self, model: str, attempt: int, success: bool, error: str = ""):
        """
        Specialized logging for API calls.
        """
        timestamp = self.get_timestamp()
        status = "SUCCESS" if success else "FAILED"
        message = f"[{timestamp}] API Call | Model: {model} | Attempt: {attempt} | Status: {status}"
        if error:
            message += f" | Error: {error}"
        self.info(message)