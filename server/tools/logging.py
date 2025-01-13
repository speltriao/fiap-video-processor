import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set default log level (can be DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log"),  # Log to file (you can adjust the file path if needed)
    ],
)
logger = logging.getLogger(__name__)
