import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine

LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

def log_setup() -> None:
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


def build_engine() -> Engine:
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    engine = build_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}")

    return engine
