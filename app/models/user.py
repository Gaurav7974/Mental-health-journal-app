from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class UserModel:
    collection = db["users"]

    @staticmethod
    def create_user(name, email, password):
        hashed = generate_password_hash(password)
        user = {
            "name": name,
            "email": email.lower(),
            "password": hashed,
            "created_at": datetime.utcnow()
        }
        UserModel.collection.insert_one(user)
        return user

    @staticmethod
    def find_by_email(email):
        return UserModel.collection.find_one({"email": email.lower()})

    @staticmethod
    def verify_password(hashed_password, password):
        return check_password_hash(hashed_password, password)
