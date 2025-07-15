# Import necessary modules
import logging
import os
from datetime import datetime

# Define the directory where logs will be saved
LOGS_DIR = "logs"

# Create the log directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate a log file name with the current date, e.g., log_2025-06-30.log
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure the logging settings:
# - Write logs to the LOG_FILE
# - Format includes timestamp, log level, and message
# - Log level is set to INFO (logs INFO, WARNING, ERROR, etc.)
logging.basicConfig(
    filename=LOG_FILE,
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


# Function to get a named logger
def get_logger(name):
    # Create or retrieve a logger with the given name
    logger = logging.getLogger(name)
    # Set the logging level to INFO
    logger.setLevel(logging.INFO)
    return logger
