from flask import Blueprint, request, render_template, session, redirect, url_for 
import logging 
from typing import Optional 
from database.models.tables.appointments import Appointment 
from managers.appointment import update_prescription 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
DOCTORS_BLUEPRINT = Blueprint('doctors', __name__) 
USERS_LOGIN = 'users.login' 
@DOCTORS_BLUEPRINT.route('', methods=['POST']) 
def index() -> None: 
    logger.info("Doctor index accessed.") 
    # Placeholder for future implementation 
    pass 
@DOCTORS_BLUEPRINT.route('/appointments', methods=['GET']) 
def appointments() -> str: 
    if session.get('user_type') == 'DOCTOR': 
        try: 
            all_appointments = Appointment.get_by_doctor_id(session.get('user_idx')) 
            context = { 
                'all_appointments': all_appointments 
            } 
            logger.info("Doctor viewing all appointments.") 
            return render_template('doctor_all_appointments.html', **context) 
        except Exception as e: 
            logger.error("Error retrieving appointments: %s", e, exc_info=True) 
            return redirect(url_for('users.logout')) 
    else: 
        logger.warning("Unauthorized access attempt to doctor appointments page.") 
        return redirect(url_for('users.logout')) 
@DOCTORS_BLUEPRINT.route('/appointments/<idx>', methods=['POST']) 
def prescription(idx: str) -> str: 
    if session.get('user_type') == 'DOCTOR': 
        try: 
            prescription_text = request.form.get('prescription') 
            update_prescription(idx, prescription_text) 
            logger.info("Prescription updated for appointment: %s", idx) 
            return redirect(url_for('doctors.appointments')) 
        except Exception as e: 
            logger.error("Error updating prescription: %s", e, exc_info=True) 
            return redirect(url_for('doctors.appointments')) 
    else: 
        logger.warning("Unauthorized access attempt to update prescription.") 
        return redirect(url_for('users.logout'))