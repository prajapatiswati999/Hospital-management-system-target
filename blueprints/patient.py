from flask import Blueprint, render_template, session, redirect, url_for 
import logging 
from typing import Optional 
from database.models.tables.appointments import Appointment 
from database.models.tables.doctors import Doctor 
from managers.slot import get_slot_by_doctor_id, book_slot, get_doctor_name 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
PATIENTS_BLUEPRINT = Blueprint('patients', __name__) 
USERS_LOGIN = 'users.login' 
@PATIENTS_BLUEPRINT.route('', methods=['POST']) 
def index() -> None: 
    logger.info("Patient index accessed.") 
    # Placeholder for future implementation 
    pass 
@PATIENTS_BLUEPRINT.route('/doctors', methods=['GET']) 
def doctors() -> str: 
    try: 
        all_doctors = Doctor.get_all_doctors() 
        context = { 
            'all_doctors': all_doctors 
        } 
        logger.info("Patient viewing all doctors.") 
        return render_template('patient_all_doctors.html', **context) 
    except Exception as e: 
        logger.error("Error retrieving doctors: %s", e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN)) 
@PATIENTS_BLUEPRINT.route('/doctors/<idx>', methods=['GET']) 
def view_doctor_slots(idx: str) -> str: 
    try: 
        slots = get_slot_by_doctor_id(idx) 
        doc_name = get_doctor_name(idx) 
        context = { 
            'slots': slots, 
            'doctor_id': idx, 
            'doc_name': doc_name 
        } 
        logger.info("Patient viewing slots for doctor: %s", idx) 
        return render_template('doctor_all_slots.html', **context) 
    except Exception as e: 
        logger.error("Error retrieving slots for doctor %s: %s", idx, e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN)) 
@PATIENTS_BLUEPRINT.route('/doctors/<doctor_id>/<patient_id>/book/<slot_id>/<slot_number>', methods=['GET']) 
def book(doctor_id: str, patient_id: str, slot_id: str, slot_number: str) -> str: 
    try: 
        book_slot(slot_id, doctor_id, patient_id, slot_number) 
        slots = get_slot_by_doctor_id(doctor_id) 
        context = { 
            'slots': slots, 
            'doctor_id': doctor_id 
        } 
        logger.info("Patient %s booked slot %s for doctor %s", patient_id, slot_number, doctor_id) 
        return render_template('doctor_all_slots.html', **context) 
    except Exception as e: 
        logger.error("Error booking slot %s for doctor %s: %s", slot_number, doctor_id, e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN)) 
@PATIENTS_BLUEPRINT.route('/appointments', methods=['GET']) 
def appointments() -> str: 
    try: 
        all_appointments = Appointment.get_by_patient_id(session.get('user_idx')) 
        context = { 
            'all_appointments': all_appointments 
        } 
        logger.info("Patient viewing all appointments.") 
        return render_template('doctor_all_appointments.html', **context) 
    except Exception as e: 
        logger.error("Error retrieving appointments: %s", e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN)) 
@PATIENTS_BLUEPRINT.route('/appointments/<idx>', methods=['GET']) 
def view_appointment(idx: str) -> str: 
    try: 
        prescription_text = Appointment.get(idx).prescription_text 
        context = { 
            'prescription_text': prescription_text, 
            'appointment_idx': idx 
        } 
        logger.info("Patient viewing appointment: %s", idx) 
        return render_template('view_prescription.html', **context) 
    except Exception as e: 
        logger.error("Error retrieving appointment %s: %s", idx, e, exc_info=True) 
        return redirect(url_for(USERS_LOGIN))