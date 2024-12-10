import logging

# Configure the global logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Create a logger instance
logger = logging.getLogger(__name__)