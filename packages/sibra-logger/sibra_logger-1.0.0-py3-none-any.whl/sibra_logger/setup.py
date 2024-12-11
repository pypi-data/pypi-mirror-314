import logging
import logging.config
import yaml
import os
import threading
import time
from .config import LOG_CONFIG_FILE
import signal

# Global variables for logging
monitor_stop_event = threading.Event()  # Event to signal monitor thread to stop
queue_listener = None  # For managing asynchronous logging

def setup_logging(config_file=None):
    """
    Set up logging configuration from a YAML file.
    Falls back to basic configuration if the file is not found or invalid.
    """
    if config_file is None:
        config_file = LOG_CONFIG_FILE

    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        # Ensure the log directory exists
        for handler_name, handler_config in config.get("handlers", {}).items():
            if handler_config.get("class") == "logging.handlers.RotatingFileHandler":
                filename = handler_config.get("filename")
                if filename:
                    os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Configure logging
        logging.config.dictConfig(config)
        logging.getLogger().info("Logging configuration loaded.")
    except Exception as e:
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().exception(f"Failed to load logging configuration: {e}")
        logging.getLogger().warning(f"Failed to load logging configuration: {e}. Using basic configuration.")


def monitor_config(config_file=None, check_interval=10):
    """
    Monitor the configuration file for changes and reload logging configuration dynamically.
    """
    if config_file is None:
        config_file = LOG_CONFIG_FILE
    last_mtime = 0
    while not monitor_stop_event.is_set():
        try:
            current_mtime = os.path.getmtime(config_file)
            if current_mtime != last_mtime:
                setup_logging(config_file)
                logging.getLogger().info("Logging configuration reloaded.")
                last_mtime = current_mtime
        except FileNotFoundError:
            logging.getLogger().warning(f"Configuration file not found: {config_file}. Retrying...")
        except Exception as e:
            logging.getLogger().error(f"Error monitoring configuration file: {e}")
        time.sleep(check_interval)


def start_logging_monitor(config_file=None):
    """
    Start the configuration monitoring in a separate thread.
    """
    if config_file is None:
        config_file = LOG_CONFIG_FILE

    global monitor_stop_event
    monitor_stop_event.clear()  # Ensure the event is cleared before starting the thread
    monitor_thread = threading.Thread(target=monitor_config, args=(config_file,), daemon=True)
    monitor_thread.start()


def stop_logging():
    """
    Stop the configuration monitoring thread and any asynchronous logging operations.
    """
    global monitor_stop_event, queue_listener

    # Signal the monitor thread to stop
    monitor_stop_event.set()

    # Stop the queue listener if running
    if queue_listener:
        queue_listener.stop()
        queue_listener = None

    logging.getLogger().info("Logging Stopped")


def remove_all_handlers():
    """
    Remove all handlers from all loggers.
    """
    root_logger = logging.getLogger()
    handlers = root_logger.handlers[:]
    for handler in handlers:
        root_logger.removeHandler(handler)
        handler.close()

    logging.getLogger().info("All logging handlers have been removed.")

def close_file_handlers():
    """
    Close all file-based handlers in the root logger.
    """
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            handler.close()

    logging.getLogger().info("All file handlers have been closed.")


def cleanup_logging():
    """
    Perform all necessary cleanup for logging resources.
    """
    stop_logging()         # Stop monitoring and asynchronous logging
    close_file_handlers()  # Close all file handlers
    remove_all_handlers()  # Remove all handlers from loggers
    logging.shutdown()     # Perform logging system shutdown
    

def cleanup_on_exit(signum, frame):
    """
    Signal handler that calls cleanup_logging.
    """
    logging.getLogger().info(f"Received signal {signum}, performing cleanup...")
    cleanup_logging()
    exit(0)


# Register signal handlers for graceful cleanup
signal.signal(signal.SIGINT, cleanup_on_exit)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, cleanup_on_exit)  # Handle termination s