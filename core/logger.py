# import logging
# import os
#
# # Ensure logs directory exists
# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)
#
# # Define log file path
# LOG_FILE = os.path.join(LOG_DIR, "app.log")
#
# # Configure the logger
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )
#
# # Provide a logger instance for use across the app
# logger = logging.getLogger("NaiveBayesApp")

import logging
import os

# Determine absolute path to logs directory, relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Define full log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Provide a logger instance for use across the app
logger = logging.getLogger("NaiveBayesApp")

