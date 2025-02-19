from datetime import datetime 
from uuid import uuid4 
import logging 
from typing import List, Optional 
from database.models.tables.doctors import Doctor 
from database.models.tables.slots import Slot 
from managers.appointment import create_appointment 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
DATE_FORMAT = '%Y-%m-%d' 
def create_slot(doctor_id: str, date: str, slots: List[Optional[str]]) -> None: 
    try: 
        Slot.create(idx=str(uuid4()), doctor_id=doctor_id, date=datetime.strptime(date, DATE_FORMAT), 
                    slot1=slots[0] or 'False', slot2=slots[1] or 'False', 
                    slot3=slots[2] or 'False', slot4=slots[3] or 'False') 
        logger.info("Slot created successfully for doctor: %s on date: %s", doctor_id, date) 
    except Exception as e: 
        logger.error("Error creating slot for doctor %s on date %s: %s", doctor_id, date, e, exc_info=True) 
def get_slot_by_doctor_id(doctor_id: str) -> List[Slot]: 
    try: 
        slots = Slot.get_by_doctor_id(doctor_id) 
        logger.info("Retrieved slots for doctor with id: %s", doctor_id) 
        return slots 
    except Exception as e: 
        logger.error("Error retrieving slots for doctor with id %s: %s", doctor_id, e, exc_info=True) 
        return [] 
def book_slot(slot_id: str, doctor_id: str, patient_id: str, slot_number: str) -> None: 
    try: 
        slot = Slot.get(slot_id) 
        if not slot: 
            logger.warning("Slot not found with id: %s", slot_id) 
            return 
        if slot_number == 'Slot1': 
            slot.slot1 = patient_id 
        elif slot_number == 'Slot2': 
            slot.slot2 = patient_id 
        elif slot_number == 'Slot3': 
            slot.slot3 = patient_id 
        elif slot_number == 'Slot4': 
            slot.slot4 = patient_id 
        slot.save() 
        create_appointment(doctor_id=doctor_id, patient_id=patient_id, slot_number=slot_number, date=slot.date) 
        logger.info("Slot %s booked for patient %s with doctor %s", slot_number, patient_id, doctor_id) 
    except Exception as e: 
        logger.error("Error booking slot %s for doctor %s: %s", slot_number, doctor_id, e, exc_info=True) 
def get_doctor_name(doc_idx: str) -> str: 
    try: 
        doctor = Doctor.get(doc_idx) 
        if not doctor: 
            logger.warning("Doctor not found with id: %s", doc_idx) 
            return "Unknown Doctor" 
        doc_first_name, doc_last_name = doctor.user.first_name, doctor.user.last_name 
        doc_name = f'{doc_first_name} {doc_last_name}' 
        logger.info("Retrieved doctor name: %s", doc_name) 
        return doc_name 
    except Exception as e: 
        logger.error("Error retrieving doctor name for id %s: %s", doc_idx, e, exc_info=True) 
        return "Unknown Doctor"