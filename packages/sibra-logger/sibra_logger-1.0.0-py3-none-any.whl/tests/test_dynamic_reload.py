import yaml
import logging
from sibra_logger import setup_logging, start_logging_monitor, cleanup_logging
import time

def test_dynamic_reloading():
    config_file = "sibra_logger/log_config.yaml"
    with open(config_file, "r") as f:
        original_config = yaml.safe_load(f)

    updated_config = original_config.copy()
    updated_config["handlers"]["console"]["level"] = "DEBUG"
    with open(config_file, "w") as f:
        yaml.dump(updated_config, f)

    setup_logging()
    start_logging_monitor()
    logger = logging.getLogger("sibra_logger")
    logger.debug("This is a debug message after reload.")

    # Restore original config
    with open(config_file, "w") as f:
        yaml.dump(original_config, f)

    cleanup_logging()