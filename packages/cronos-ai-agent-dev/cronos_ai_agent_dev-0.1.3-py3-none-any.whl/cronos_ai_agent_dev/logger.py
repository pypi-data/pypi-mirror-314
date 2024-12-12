import logging
import os

# Get the log level from an environment variable, default to INFO if not set
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
# Configure the global logger
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)