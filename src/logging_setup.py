import os
import logging
from dotenv import load_dotenv

def log_setup():

    load_dotenv()
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        handlers=[logging.StreamHandler()]
    )

    log = logging.getLogger(__name__)
    log.info(f"Logging is started, level {log_level_str}")