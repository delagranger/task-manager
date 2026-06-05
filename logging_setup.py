import os
import logging
from dotenv import load_dotenv

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def log_setup():
    load_dotenv()
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    if log_level_str not in LOG_LEVELS:
        print(f"WARNING: Incorrect log level '{log_level_str}, using level INFO'")
        log_level_str = "INFO"
    log_level = getattr(logging, log_level_str)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[logging.StreamHandler()]
    )

    log = logging.getLogger(__name__)
    log.info(f"Logging is started with level {log_level_str}")