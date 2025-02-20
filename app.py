from flask import Flask, redirect, url_for
from database.db import db
from blueprints.users import USERS_BLUEPRINT
from blueprints.doctor import DOCTORS_BLUEPRINT
from blueprints.admin import ADMIN_BLUEPRINT
from blueprints.patient import PATIENTS_BLUEPRINT
import logging
from logging.handlers import RotatingFileHandler
import os
 
# Check for Python 3.12 NOTICE level support
if not hasattr(logging, "NOTICE"):
    logging.NOTICE = 25
    logging.addLevelName(logging.NOTICE, "NOTICE")
 
# Configure logging
LOG_FILE = "app.log"
 
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
 
# Rotating file handler to avoid log bloat
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=2000, backupCount=5)
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(file_handler)
 
app = Flask(__name__)
 
# Ensure configuration file exists before loading
CONFIG_PATH = "config/settings.staging.cfg"
 
try:
    if os.path.exists(CONFIG_PATH):
        app.config.from_pyfile(CONFIG_PATH)
        logger.log(logging.NOTICE, f"Configuration loaded successfully from {CONFIG_PATH}.")
    else:
        raise FileNotFoundError(f"Configuration file '{CONFIG_PATH}' not found.")
except FileNotFoundError as e:
    logger.error(f"Configuration file not found: {e}", exc_info=True)
    exit(1)  # Stop execution if critical config is missing
except Exception as e:
    logger.error(f"Error loading configuration file: {e}", exc_info=True)
    exit(1)
 
# Initialize database
db.init_app(app)
 
# Register blueprints
app.register_blueprint(USERS_BLUEPRINT, url_prefix='/users')
app.register_blueprint(DOCTORS_BLUEPRINT, url_prefix='/doctors')
app.register_blueprint(ADMIN_BLUEPRINT, url_prefix='/admin')
app.register_blueprint(PATIENTS_BLUEPRINT, url_prefix='/patients')
 
@app.before_request
def create_tables():
    """Ensure database tables exist before handling requests."""
    try:
        with app.app_context():
            db.create_all()
        logger.info("Database tables verified/created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}", exc_info=True)
 
@app.route('/')
def index():
    """Redirects to user registration page."""
    logger.info("Redirecting to user registration page.")
    return redirect(url_for('users.register_user'))
 
if __name__ == '__main__':
    try:
        app.run(debug=True)
        logger.log(logging.NOTICE, "Flask application started successfully.")
    except Exception as e:
        logger.error(f"Error starting Flask application: {e}", exc_info=True)