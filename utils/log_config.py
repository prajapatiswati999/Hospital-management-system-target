import logging

from logging.handlers import RotatingFileHandler
# Define NOTICE level if not available (Python 3.12+)
if not hasattr(logging, "NOTICE"):
    logging.NOTICE = 25  # Default NOTICE level value
    logging.addLevelName(logging.NOTICE, "NOTICE")
 
# Configure logging
def setup_logging():
    try:
        # Create a logger
        logger = logging.getLogger('app_logger')
        logger.setLevel(logging.INFO)  # Set to INFO for production
 
        # Create handlers
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
 
        file_handler = RotatingFileHandler('app.log', maxBytes=2000, backupCount=5)
        file_handler.setLevel(logging.DEBUG)
 
        # Create formatters and add them to handlers
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
 
        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
 
        # Test NOTICE level logging
        logger.log(logging.NOTICE, "This is a NOTICE level log.")  
 
        logger.info("Logging is set up.")
    
    except Exception as e:
        logging.error(f"Failed to set up logging: {e}", exc_info=True)
        raise
 
# Initialize logging setup
setup_logging()