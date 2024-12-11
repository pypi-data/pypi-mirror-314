# SIBRA Logger

SIBRA Logger is an configurable logging library designed for Python applications. It supports dynamic configuration reloading,  structured logging for seamless integration into any project.

---

## Features

1. **Dynamic Configuration Reloading**:
   - Automatically monitors and reloads logging configurations without restarting the application.



---

## Installation

### Prerequisites

- Python 3.6 or higher.

### Install the Package

```
pip install sibra_logger

```

# Install Development Dependencies (Optional)
  To install dependencies for development and testing:

```
pip install sibra_logger[dev]
```

# Usage
## Basic Setup
  1. Initialize Logging in Your Application

```
from sibra_logger import setup_logging, start_logging_monitor

# Set up logging
setup_logging()

# Start monitoring configuration changes
start_logging_monitor()
```

  2. Log Messages

```
import logging

logger = logging.getLogger(__name__)

logger.info("This is an informational message.")
logger.debug("This is a debug message.")
logger.error("This is an error message.")
```
## Using a Custom Configuration File
Pass a custom configuration file path to setup_logging:

```
setup_logging("path/to/custom_config.yaml")
```

## Storing configuration file as env variable
This logger support storing env variable SIBRA_LOG_CONFIG & pulls the config file from env variable as well.

# Configuration
The logging behavior is controlled via a YAML configuration file (log_config.yaml).

## Example Configuration
```
version: 1
disable_existing_loggers: false

formatters:
  detailed:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s [Line: %(lineno)d]'
    datefmt: '%Y-%m-%d %H:%M:%S'


handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: detailed
    stream: ext://sys.stdout
  rotating_file:
    class: logging.handlers.RotatingFileHandler
    level: INFO
    formatter: detailed
    filename: logs/rotating_app.log
    maxBytes: 10485760
    backupCount: 5
    encoding: utf8


root:
  level: INFO
  handlers: [console, rotating_file]
```





# Dependencies
## Required
pyyaml: For YAML configuration.


#Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and submit a pull request.

# License
This project is licensed under the MIT License. See LICENSE for more details.

This README.md reflects the features and functionality of your package, organized to be user-friendly and professional. 
Let me know if you'd like any additional adjustments!

