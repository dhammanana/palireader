import logging
import datetime
import os
import re
from colorama import init, Fore, Style
from logging.handlers import RotatingFileHandler

# Initialize colorama for cross-platform colored output
init(autoreset=True)

def get_logger(log_file="log/app.log", bold_numbers=False):
    """
    Configure the logger singleton with file and console handlers.
    Call this function once at the start of the application.
    """
    # Get the logger instance
    logger = logging.getLogger("AppLogger")
    
    # Prevent reconfiguring if already set up
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # Create log directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # File handler
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)  # 10MB per file, keep 5 backups
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler with colorized output
    class ColorFormatter(logging.Formatter):
        def __init__(self, bold_numbers=False, fmt=None, datefmt=None):
            super().__init__(fmt=fmt, datefmt=datefmt)
            self.bold_numbers = bold_numbers
            self.level_colors = {
                "DEBUG": Fore.WHITE,
                "INFO": Fore.GREEN,
                "WARNING": Fore.YELLOW,
                "ERROR": Fore.RED,
                "CRITICAL": Fore.MAGENTA
            }
        
        def format(self, record):
            # Get the original message
            message = record.getMessage()
            
            # Apply bold style to numbers and slashes if enabled
            if self.bold_numbers:
                message = re.sub(r'([\d/]+)', f"{Style.BRIGHT}\\1{Style.NORMAL}", message)
            # Apply bold style to text in square brackets
            message = re.sub(r"\[(.*?)\]", f"{Style.BRIGHT}\\1{Style.NORMAL}", message)
            
            # Apply color based on log level
            color = self.level_colors.get(record.levelname, Fore.WHITE)
            formatted_message = f"{color}{message}{Style.RESET_ALL}"
            
            # Return the formatted record
            record.msg = formatted_message
            return super().format(record)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColorFormatter(
        bold_numbers=bold_numbers,
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Example usage
if __name__ == "__main__":
    # Configure the logger once
    logger = get_logger(log_file="assets/app.log", bold_numbers=True)
    
    # Use the logger throughout the application
    logger.debug("This is a debug message with numbers 123/456")
    logger.info("This is an info message [SUCCESS]")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Simulate multiple modules using the same logger
    logger2 = get_logger()  # No duplicate handlers
    logger2.info("This is another info message [TEST]")