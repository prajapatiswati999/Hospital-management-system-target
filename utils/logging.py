import logging 
from logging.handlers import RotatingFileHandler 
# Configure logging 
def setup_logging(): 
    try: 
        # Create a logger 
        logger = logging.getLogger('app_logger') 
        logger.setLevel(logging.INFO)  # Set to INFO to reduce excessive logging in production 
        # Create handlers 
        console_handler = logging.StreamHandler() 
        console_handler.setLevel(logging.INFO) 
        file_handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5) 
        file_handler.setLevel(logging.DEBUG) 
        # Create formatters and add them to handlers 
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
        console_handler.setFormatter(console_format) 
        file_handler.setFormatter(file_format) 
        # Add handlers to the logger 
        logger.addHandler(console_handler) 
        logger.addHandler(file_handler) 
        logger.info("Logging is set up.") 
    except Exception as e: 
        logging.error(f"Failed to set up logging: {e}", exc_info=True) 
        raise 
# Initialize logging setup 
setup_logging()