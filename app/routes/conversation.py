from flask import Blueprint, request, jsonify
from app.controllers.conversation_controller import handle_conversation
from app.utils.decorators import jwt_required_user

conversation_bp = Blueprint("conversation", __name__)

@conversation_bp.route("/", methods=["POST"])
@jwt_required_user
def converse(user_id):
    data = request.json

    if not data or "message" not in data:
        return jsonify({"msg": "message field required"}), 400

    result, code = handle_conversation(user_id, data["message"])
    return jsonify(result), code
