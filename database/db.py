from flask_sqlalchemy import SQLAlchemy 
import logging 
# Initialize the SQLAlchemy database instance 
db = SQLAlchemy() 
def init_db(app): 
    try: 
        logger = logging.getLogger('app_logger') 
        logger.info("Initializing database with app configuration") 
        db.init_app(app) 
        logger.info("Database initialized successfully") 
    except Exception as e: 
        logger.error(f"Unexpected error initializing database: {e}", exc_info=True) 
        raise