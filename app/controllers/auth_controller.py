from flask_jwt_extended import create_access_token
from app.models.user import UserModel
from datetime import timedelta

def register_user(data):
    required = ["name", "email", "password"]

    if not all(k in data for k in required):
        return {"msg": "Missing fields"}, 400

    if UserModel.find_by_email(data["email"]):
        return {"msg": "Email already exists"}, 400

    user = UserModel.create_user(
        data["name"],
        data["email"],
        data["password"]
    )

    return {"msg": "User registered successfully"}, 201


def login_user(data):
    if "email" not in data or "password" not in data:
        return {"msg": "Missing email or password"}, 400

    user = UserModel.find_by_email(data["email"])
    if not user:
        return {"msg": "Invalid credentials"}, 401

    if not UserModel.verify_password(user["password"], data["password"]):
        return {"msg": "Invalid credentials"}, 401

    token = create_access_token(
        identity=str(user["_id"]),
        expires_delta=timedelta(days=7)
    )

    return {
        "msg": "Login successful",
        "token": token,
        "user": {
            "name": user["name"],
            "email": user["email"]
        }
    }, 200
