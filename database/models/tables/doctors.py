from database.db import db 
from ..enums.domains import Domain 
from ..enums.user_types import UserType 
from ..tables.users import User 
import logging 
from typing import Optional, List 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class Doctor(db.Model): 
    __tablename__ = 'doctors' 
    idx = db.Column(db.String, db.ForeignKey('users.idx'), primary_key=True) 
    domain = db.Column(db.Enum(Domain)) 
    user = db.relationship('User', backref=db.backref('doctor', cascade="delete, delete-orphan"), lazy=True, 
                           single_parent=True) 
    @classmethod 
    def get(cls, pk: str) -> Optional['Doctor']: 
        try: 
            doctor = cls.query.get(pk) 
            logger.info("Retrieved doctor with id: %s", pk) 
            return doctor 
        except Exception as e: 
            logger.error("Error retrieving doctor with id %s: %s", pk, e, exc_info=True) 
            return None 
    @classmethod 
    def get_by_uid(cls, idx: str) -> Optional['Doctor']: 
        try: 
            user = cls.query.filter_by(idx=idx).first() 
            logger.info("Retrieved doctor by uid: %s", idx) 
            return user 
        except Exception as e: 
            logger.error("Error retrieving doctor by uid %s: %s", idx, e, exc_info=True) 
            return None 
    @classmethod 
    def get_by_username(cls, username: str) -> Optional['Doctor']: 
        try: 
            user = cls.query.filter_by(username=username).first() 
            logger.info("Retrieved doctor by username: %s", username) 
            return user 
        except Exception as e: 
            logger.error("Error retrieving doctor by username %s: %s", username, e, exc_info=True) 
            return None 
    @classmethod 
    def get_all_doctors(cls) -> List['Doctor']: 
        try: 
            doctors = cls.query.all() 
            logger.info("Retrieved all doctors") 
            return doctors 
        except Exception as e: 
            logger.error("Error retrieving all doctors: %s", e, exc_info=True) 
            return [] 
    @classmethod 
    def create(cls, **kwargs) -> Optional['Doctor']: 
        user = User(idx=kwargs.get('idx'), username=kwargs.get('username'), password=kwargs.get('password'), 
                    first_name=kwargs.get('first_name'), last_name=kwargs.get('last_name'), 
                    age=kwargs.get('age'), user_type=UserType(kwargs.get('user_type'))) 
        instance = cls(idx=kwargs.get('idx'), domain=Domain(kwargs.get('domain')), user=user) 
        try: 
            saved_instance = instance.save() 
            logger.info("Created doctor with id: %s", saved_instance.idx) 
            return saved_instance 
        except Exception as e: 
            logger.error("Error creating doctor: %s", e, exc_info=True) 
            return None 
    def save(self, commit: bool = True) -> 'Doctor': 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Saved doctor with id: %s", self.idx) 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving doctor with id %s: %s", self.idx, e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit: bool = True) -> bool: 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Deleted doctor with id: %s", self.idx) 
                return True 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting doctor with id %s: %s", self.idx, e, exc_info=True) 
                return False 
        return True