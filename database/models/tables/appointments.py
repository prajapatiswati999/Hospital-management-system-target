from database.db import db 
from typing import Optional, List 
import logging 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Appointment(db.Model): 
    __tablename__ = 'appointments' 
    idx = db.Column(db.String, primary_key=True) 
    doctor_id = db.Column(db.String, db.ForeignKey('users.idx')) 
    patient_id = db.Column(db.String, db.ForeignKey('users.idx')) 
    slot_number = db.Column(db.String) 
    date = db.Column(db.Date) 
    prescription_text = db.Column(db.Text, default='') 
    doctor = db.relationship('User', backref=db.backref('appointment_doctor', cascade="delete, delete-orphan"), 
                             lazy=True, 
                             single_parent=True, foreign_keys='Appointment.doctor_id') 
    patient = db.relationship('User', backref=db.backref('appointment_patient', cascade="delete, delete-orphan"), 
                              lazy=True, 
                              single_parent=True, foreign_keys='Appointment.patient_id') 
    @classmethod 
    def get(cls, pk: str) -> Optional['Appointment']: 
        try: 
            appointment = cls.query.get(pk) 
            logger.info("Retrieved appointment with id: %s", pk) 
            return appointment 
        except Exception as e: 
            logger.error("Error retrieving appointment with id %s: %s", pk, e, exc_info=True) 
            return None 
    @classmethod 
    def get_by_doctor_id(cls, idx: str) -> List['Appointment']: 
        try: 
            appointments = cls.query.filter_by(doctor_id=idx).all() 
            logger.info("Retrieved appointments for doctor with id: %s", idx) 
            return appointments 
        except Exception as e: 
            logger.error("Error retrieving appointments for doctor with id %s: %s", idx, e, exc_info=True) 
            return [] 
    @classmethod 
    def get_by_patient_id(cls, idx: str) -> List['Appointment']: 
        try: 
            appointments = cls.query.filter_by(patient_id=idx).all() 
            logger.info("Retrieved appointments for patient with id: %s", idx) 
            return appointments 
        except Exception as e: 
            logger.error("Error retrieving appointments for patient with id %s: %s", idx, e, exc_info=True) 
            return [] 
    @classmethod 
    def create(cls, **kwargs) -> Optional['Appointment']: 
        instance = cls(**kwargs) 
        try: 
            saved_instance = instance.save() 
            logger.info("Created appointment with id: %s", saved_instance.idx) 
            return saved_instance 
        except Exception as e: 
            logger.error("Error creating appointment: %s", e, exc_info=True) 
            return None 
    def save(self, commit: bool = True) -> 'Appointment': 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Saved appointment with id: %s", self.idx) 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving appointment with id %s: %s", self.idx, e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit: bool = True) -> bool: 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Deleted appointment with id: %s", self.idx) 
                return True 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting appointment with id %s: %s", self.idx, e, exc_info=True) 
                return False 
        return True