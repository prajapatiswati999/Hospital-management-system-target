from database.db import db 
import logging 
from typing import Optional, List 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Slot(db.Model): 
    __tablename__ = 'slots' 
    idx = db.Column(db.String, primary_key=True) 
    doctor_id = db.Column(db.String) 
    slot1 = db.Column(db.String) 
    slot2 = db.Column(db.String) 
    slot3 = db.Column(db.String) 
    slot4 = db.Column(db.String) 
    date = db.Column(db.Date) 
    @classmethod 
    def get(cls, pk: str) -> Optional['Slot']: 
        try: 
            slot = cls.query.get(pk) 
            logger.info("Retrieved slot with id: %s", pk) 
            return slot 
        except Exception as e: 
            logger.error("Error retrieving slot with id %s: %s", pk, e, exc_info=True) 
            return None 
    @classmethod 
    def get_all(cls) -> List['Slot']: 
        try: 
            slots = cls.query.all() 
            logger.info("Retrieved all slots") 
            return slots 
        except Exception as e: 
            logger.error("Error retrieving all slots: %s", e, exc_info=True) 
            return [] 
    @classmethod 
    def get_by_doctor_id(cls, idx: str) -> List['Slot']: 
        try: 
            slots = cls.query.filter_by(doctor_id=idx).all() 
            logger.info("Retrieved slots for doctor with id: %s", idx) 
            return slots 
        except Exception as e: 
            logger.error("Error retrieving slots for doctor with id %s: %s", idx, e, exc_info=True) 
            return [] 
    @classmethod 
    def get_by_patient_id(cls, idx: str) -> List['Slot']: 
        try: 
            slots = cls.query.filter_by(idx=idx).all() 
            logger.info("Retrieved slots for patient with id: %s", idx) 
            return slots 
        except Exception as e: 
            logger.error("Error retrieving slots for patient with id %s: %s", idx, e, exc_info=True) 
            return [] 
    @classmethod 
    def create(cls, **kwargs) -> Optional['Slot']: 
        instance = cls(**kwargs) 
        try: 
            saved_instance = instance.save() 
            logger.info("Created slot with id: %s", saved_instance.idx) 
            return saved_instance 
        except Exception as e: 
            logger.error("Error creating slot: %s", e, exc_info=True) 
            return None 
    def save(self, commit: bool = True) -> 'Slot': 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Saved slot with id: %s", self.idx) 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving slot with id %s: %s", self.idx, e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit: bool = True) -> bool: 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Deleted slot with id: %s", self.idx) 
                return True 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting slot with id %s: %s", self.idx, e, exc_info=True) 
                return False 
        return True