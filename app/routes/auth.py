from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import register_user, login_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    try:
        result, code = register_user(data)
        return jsonify(result), code
    except Exception as e:
        return jsonify({"message": "Registration failed", "error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid or missing JSON body"}), 400

    try:
        result, code = login_user(data)
        return jsonify(result), code
    except Exception as e:
        return jsonify({"message": "Login failed", "error": str(e)}), 500
