import logging
from sibra_logger import setup_logging, cleanup_logging

class InMemoryHandler(logging.Handler):
    """Custom handler to capture logs in memory for testing."""
    def __init__(self):
        super().__init__()
        self.log_records = []

    def emit(self, record):
        self.log_records.append(self.format(record))

def test_logging_output():
    # Setup logging
    setup_logging()

    # Add in-memory handler
    memory_handler = InMemoryHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    memory_handler.setFormatter(formatter)

    logger = logging.getLogger("sibra_logger")
    logger.addHandler(memory_handler)

    # Ensure the logger level is DEBUG for testing
    logger.setLevel(logging.DEBUG)

    # Emit test logs
    logger.debug("Debug message.")
    logger.info("Info message.")
    logger.error("Error message.")

    # Assert logs are captured in memory
    captured_logs = memory_handler.log_records
    assert any("Debug message." in log for log in captured_logs)
    assert any("Info message." in log for log in captured_logs)
    assert any("Error message." in log for log in captured_logs)

    # Cleanup logging
    logger.removeHandler(memory_handler)
    cleanup_logging()