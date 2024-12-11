import logging
from sibra_logger import setup_logging, cleanup_logging

def test_cleanup_logging():
    setup_logging()
    logger = logging.getLogger("sibra_logger")
    logger.info("Testing cleanup.")
    cleanup_logging()
    assert len(logging.getLogger().handlers) == 0