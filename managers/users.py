from database.models.tables.users import User 
from database.models.tables.doctors import Doctor 
from database.models.enums.user_types import UserType 
from database.models.enums.domains import Domain 
from uuid import uuid4 
import logging 
from typing import Optional 
# Configure logging 
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__) 
def create_user(username: str, password: str, first_name: str, last_name: str, age: Optional[int], domain: str, user_type: str) -> None: 
    idx = str(uuid4()) 
    try: 
        if user_type == 'DOCTOR': 
            Doctor.create(idx=idx, username=username, password=password, first_name=first_name, 
                          last_name=last_name, domain=Domain(domain), 
                          age=age, user_type=UserType(user_type)) 
            logger.info("Doctor user created successfully: %s", username) 
        else: 
            User.create(idx=idx, username=username, password=password, first_name=first_name, last_name=last_name, 
                        age=age, user_type=UserType(user_type)) 
            logger.info("User created successfully: %s", username) 
    except Exception as e: 
        logger.error("Error creating user: %s", e, exc_info=True) 
        raise 
def get_user(username: str, password: str) -> Optional[User]: 
    try: 
        user = User.get_by_username(username) 
        if user and user.check_password(password): 
            logger.info("User retrieved successfully: %s", username) 
            return user 
        else: 
            logger.warning("User not found or password mismatch: %s", username) 
            return None 
    except Exception as e: 
        logger.error("Error retrieving user: %s", e, exc_info=True) 
        return None 
def delete_user(idx: str) -> None: 
    try: 
        user = User.get(idx) 
        if user: 
            user.delete() 
            logger.info("User deleted successfully: %s", idx) 
        else: 
            logger.warning("User not found for deletion: %s", idx) 
    except Exception as e: 
        logger.error("Error deleting user: %s", e, exc_info=True) 
        raise