from uuid import uuid4 
from typing import Optional 
import logging 
from database.models.tables.appointments import Appointment 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def create_appointment(doctor_id: str, patient_id: str, slot_number: str, date: str) -> Optional[Appointment]: 
    try: 
        appointment = Appointment.create(idx=str(uuid4()), doctor_id=doctor_id, patient_id=patient_id, 
                                         slot_number=slot_number, date=date) 
        if appointment: 
            logger.info("Appointment created successfully with id: %s", appointment.idx) 
        return appointment 
    except Exception as e: 
        logger.error("Error creating appointment: %s", e, exc_info=True) 
        return None 
def update_prescription(appointment_idx: str, prescription_text: str) -> bool: 
    try: 
        appointment = Appointment.get(appointment_idx) 
        if appointment: 
            appointment.prescription_text = prescription_text 
            appointment.save() 
            logger.info("Prescription updated for appointment with id: %s", appointment_idx) 
            return True 
        else: 
            logger.warning("Appointment not found with id: %s", appointment_idx) 
            return False 
    except Exception as e: 
        logger.error("Error updating prescription for appointment with id %s: %s", appointment_idx, e, exc_info=True) 
        return False