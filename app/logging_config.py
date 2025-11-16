import logging
from logging.handlers import RotatingFileHandler
import os

# --- Configuration ---
LOG_DIR = "logs"
LOG_FILE = "app.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5
LOG_LEVEL = "INFO"

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)
log_path = os.path.join(LOG_DIR, LOG_FILE)

# --- The Main Logging Configuration Dictionary ---

# This is the standard "production" formatter
prod_formatter = {
    "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(process)d] "
    "[%(filename)s:%(lineno)d] - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S %z",
}

# This is a simpler formatter for local dev/console
dev_formatter = {
    "format": "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep existing loggers (like uvicorn)
    # --- Formatters ---
    "formatters": {
        "production": prod_formatter,
        "development": dev_formatter,
    },
    # --- Handlers ---
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "development",  # Use simple format for console
            "level": LOG_LEVEL,
            "stream": "ext://sys.stdout",
        },
        "file_rotating": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "production",  # Use detailed format for files
            "level": "WARNING",  # Log only WARNING and above to the file
            "filename": log_path,
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": LOG_BACKUP_COUNT,
            "encoding": "utf-8",
        },
    },
    # --- Loggers ---
    "loggers": {
        "app": {  # Your application's logger
            "handlers": ["console", "file_rotating"],
            "level": LOG_LEVEL,
            "propagate": False,  # Don't send 'app' logs to the 'root' logger
        },
        "uvicorn": {  # Uvicorn's access logger
            "handlers": ["console", "file_rotating"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {  # Uvicorn's error logger
            "handlers": ["console", "file_rotating"],
            "level": "INFO",
            "propagate": False,
        },
    },
    # --- Root Logger ---
    "root": {
        "handlers": ["console", "file_rotating"],
        "level": "WARNING",  # Be less verbose at the root level
    },
}
