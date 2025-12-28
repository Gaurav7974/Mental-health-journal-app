from flask import Blueprint, request, jsonify
from app.controllers.mood_controller import (
    log_mood,
    get_mood_history,
    get_mood_stats
)
from app.utils.decorators import jwt_required_user

mood_bp = Blueprint("mood", __name__)

@mood_bp.route("/", methods=["POST"])
@jwt_required_user
def create(user_id):
    data = request.json
    result, code = log_mood(user_id, data)
    return jsonify(result), code


@mood_bp.route("/", methods=["GET"])
@jwt_required_user
def history(user_id):
    result, code = get_mood_history(user_id)
    return jsonify(result), code


@mood_bp.route("/stats", methods=["GET"])
@jwt_required_user
def stats(user_id):
    result, code = get_mood_stats(user_id)
    return jsonify(result), code
