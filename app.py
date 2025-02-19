from flask import Flask, redirect, url_for 
from database.db import db 
from blueprints.users import USERS_BLUEPRINT 
from blueprints.doctor import DOCTORS_BLUEPRINT 
from blueprints.admin import ADMIN_BLUEPRINT 
from blueprints.patient import PATIENTS_BLUEPRINT 
import logging 
from typing import Optional 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
app = Flask(__name__) 
# Ensure the configuration file path is correct 
try: 
    app.config.from_pyfile('config/settings.staging.cfg') 
    logger.info("Configuration loaded successfully from 'config/settings.staging.cfg'.") 
except FileNotFoundError as e: 
    logger.error("Configuration file not found: %s", e, exc_info=True) 
except Exception as e: 
    logger.error("Error loading configuration file: %s", e, exc_info=True) 
db.init_app(app) 
app.register_blueprint(USERS_BLUEPRINT, url_prefix='/users') 
app.register_blueprint(DOCTORS_BLUEPRINT, url_prefix='/doctors') 
app.register_blueprint(ADMIN_BLUEPRINT, url_prefix='/admin') 
app.register_blueprint(PATIENTS_BLUEPRINT, url_prefix='/patients') 
@app.before_request 
def create_tables() -> None: 
    try: 
        db.create_all() 
        logger.info("Database tables created successfully.") 
    except Exception as e: 
        logger.error("Error creating database tables: %s", e, exc_info=True) 
@app.route('/') 
def index() -> str: 
    logger.info("Redirecting to user registration page.") 
    return redirect(url_for('users.register_user')) 
if __name__ == '__main__': 
    try: 
        app.run(debug=True) 
        logger.info("Flask application started successfully.") 
    except Exception as e: 
        logger.error("Error starting Flask application: %s", e, exc_info=True)