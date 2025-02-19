from database.db import db 
from database.models.enums.user_types import UserType 
import bcrypt 
import logging 
from typing import Optional 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
class User(db.Model): 
    __tablename__ = 'users' 
    idx = db.Column(db.String, primary_key=True) 
    username = db.Column(db.String, unique=True) 
    first_name = db.Column(db.String) 
    last_name = db.Column(db.String) 
    age = db.Column(db.Integer, nullable=True) 
    _password_hash = db.Column(db.String) 
    user_type = db.Column(db.Enum(UserType)) 
    @property 
    def password(self) -> None: 
        raise AttributeError('Unreadable property password.') 
    @password.setter 
    def password(self, password: str) -> None: 
        if password: 
            try: 
                self._password_hash = bcrypt.hashpw( 
                    password.encode(), bcrypt.gensalt() 
                ).decode() 
                logger.info("Password hash set successfully for user: %s", self.username) 
            except Exception as e: 
                logger.error("Error setting password hash for user %s: %s", self.username, e, exc_info=True) 
                raise 
    def check_password(self, password: str) -> bool: 
        try: 
            result = bcrypt.checkpw(password.encode(), self._password_hash.encode()) 
            logger.info("Password check performed for user: %s", self.username) 
            return result 
        except Exception as e: 
            logger.error("Error checking password for user %s: %s", self.username, e, exc_info=True) 
            return False 
    @classmethod 
    def get(cls, pk: str) -> Optional['User']: 
        try: 
            user = cls.query.get(pk) 
            logger.info("Retrieved user with id: %s", pk) 
            return user 
        except Exception as e: 
            logger.error("Error retrieving user with id %s: %s", pk, e, exc_info=True) 
            return None 
    @classmethod 
    def get_by_uid(cls, idx: str) -> Optional['User']: 
        try: 
            user = cls.query.filter_by(idx=idx).first() 
            logger.info("Retrieved user by uid: %s", idx) 
            return user 
        except Exception as e: 
            logger.error("Error retrieving user by uid %s: %s", idx, e, exc_info=True) 
            return None 
    @classmethod 
    def get_by_username(cls, username: str) -> Optional['User']: 
        try: 
            user = cls.query.filter_by(username=username).first() 
            logger.info("Retrieved user by username: %s", username) 
            return user 
        except Exception as e: 
            logger.error("Error retrieving user by username %s: %s", username, e, exc_info=True) 
            return None 
    @classmethod 
    def create(cls, **kwargs) -> 'User': 
        instance = cls(**kwargs) 
        try: 
            saved_instance = instance.save() 
            logger.info("Created user with id: %s", saved_instance.idx) 
            return saved_instance 
        except Exception as e: 
            logger.error("Error creating user: %s", e, exc_info=True) 
            return None 
    def save(self, commit: bool = True) -> 'User': 
        db.session.add(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Saved user with id: %s", self.idx) 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error saving user with id %s: %s", self.idx, e, exc_info=True) 
                raise 
        return self 
    def delete(self, commit: bool = True) -> bool: 
        db.session.delete(self) 
        if commit: 
            try: 
                db.session.commit() 
                logger.info("Deleted user with id: %s", self.idx) 
                return True 
            except Exception as e: 
                db.session.rollback() 
                logger.error("Error deleting user with id %s: %s", self.idx, e, exc_info=True) 
                return False 
        return True