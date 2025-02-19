from flask import Blueprint, request, render_template, redirect, url_for, flash, session 
import logging 
from typing import Optional 
from database.models.tables.doctors import Doctor 
from managers.slot import get_slot_by_doctor_id, create_slot, get_doctor_name 
from managers.users import create_user, delete_user 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
ADMIN_BLUEPRINT = Blueprint('admin', __name__) 
USERS_LOGIN = 'users.login' 
@ADMIN_BLUEPRINT.route('', methods=['POST']) 
def index() -> None: 
    logger.info("Admin index accessed.") 
    # Placeholder for future implementation 
    pass 
@ADMIN_BLUEPRINT.route('/doctors', methods=['GET']) 
def doctors() -> str: 
    if session.get('user_type') == 'ADMIN': 
        all_doctors = Doctor.get_all_doctors() 
        context = { 
            'all_doctors': all_doctors 
        } 
        logger.info("Admin viewing all doctors.") 
        return render_template('admin_all_doctors.html', **context) 
    else: 
        logger.warning("Unauthorized access attempt to admin doctors page.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/add', methods=['GET', 'POST']) 
def add_doctor() -> str: 
    if session.get('user_type') == 'ADMIN': 
        if request.method == 'GET': 
            logger.info("Admin accessed add doctor page.") 
            return render_template('admin_add_doctor.html') 
        else: 
            username = request.form.get('username') 
            password = request.form.get('psw') 
            password_repeat = request.form.get('psw-repeat') 
            user_type = 'DOCTOR' 
            first_name = request.form.get('first-name') 
            last_name = request.form.get('last-name') 
            age = request.form.get('age') 
            domain = request.form.get('domain') or 'GENERAL' 
            if password == password_repeat: 
                try: 
                    create_user(username=username, password=password, first_name=first_name, last_name=last_name, 
                                age=age, domain=domain, user_type=user_type) 
                    logger.info("Doctor created successfully: %s", username) 
                    return redirect(url_for('admin.doctors')) 
                except Exception as err: 
                    logger.error("Error creating doctor: %s", err, exc_info=True) 
                    flash('Username already exists, please try with a different one') 
                    return redirect(url_for('admin.add_doctor')) 
            else: 
                logger.warning("Password mismatch during doctor creation.") 
                flash('Passwords do not match') 
                return redirect(url_for('users.register_user')) 
    else: 
        logger.warning("Unauthorized access attempt to add doctor page.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/delete/<idx>', methods=['GET']) 
def delete(idx: str) -> str: 
    if session.get('user_type') == 'ADMIN': 
        try: 
            delete_user(idx) 
            logger.info("Doctor deleted successfully: %s", idx) 
        except Exception as err: 
            logger.error("Error deleting doctor: %s", err, exc_info=True) 
        return redirect(url_for('admin.doctors')) 
    else: 
        logger.warning("Unauthorized access attempt to delete doctor.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/<idx>', methods=['GET']) 
def view_doctor_slots(idx: str) -> str: 
    if session.get('user_type') == 'ADMIN': 
        slots = get_slot_by_doctor_id(idx) 
        doc_name = get_doctor_name(idx) 
        context = { 
            'slots': slots, 
            'doctor_id': idx, 
            'doc_name': doc_name 
        } 
        logger.info("Admin viewing slots for doctor: %s", idx) 
        return render_template('doctor_all_slots.html', **context) 
    else: 
        logger.warning("Unauthorized access attempt to view doctor slots.") 
        return redirect(url_for('users.logout')) 
@ADMIN_BLUEPRINT.route('/doctors/<idx>/add_slot', methods=['GET', 'POST']) 
def add_slot(idx: Optional[str] = None) -> str: 
    if session.get('user_type') == 'ADMIN': 
        if request.method == 'GET': 
            doc_name = get_doctor_name(idx) 
            logger.info("Admin accessed add slot page for doctor: %s", idx) 
            return render_template('doctor_add_slot.html', **{'idx': idx, 'doc_name': doc_name}) 
        else: 
            date = request.form.get('date') 
            slot1, slot2, slot3, slot4 = request.form.get('slot1'), request.form.get('slot2'), request.form.get( 
                'slot3'), request.form.get('slot4') 
            try: 
                create_slot(doctor_id=idx, date=date, slots=[slot1, slot2, slot3, slot4]) 
                logger.info("Slot created successfully for doctor: %s", idx) 
            except Exception as err: 
                logger.error("Error creating slot: %s", err, exc_info=True) 
            return redirect(url_for('admin.view_doctor_slots', idx=idx)) 
    else: 
        logger.warning("Unauthorized access attempt to add slot.") 
        return redirect(url_for('users.logout'))