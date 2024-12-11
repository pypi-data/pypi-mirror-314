import os

# Default configuration file path
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_CONFIG_FILE = os.getenv("SIBRA_LOG_CONFIG", os.path.join(BASE_DIR, "log_config.yaml"))

MODULE_DIR = os.path.dirname(__file__)
# Fallback configuration path in the sibra_logger module folder
DEFAULT_CONFIG_FILE = os.path.join(MODULE_DIR, "log_config.yaml")

# Check for environment variable or fallback paths
LOG_CONFIG_FILE = os.getenv("SIBRA_LOG_CONFIG", os.path.join(BASE_DIR, "log_config.yaml"))
if not os.path.exists(LOG_CONFIG_FILE):  # If the file doesn't exist
    LOG_CONFIG_FILE = DEFAULT_CONFIG_FILE
    

# Directory for log files
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)