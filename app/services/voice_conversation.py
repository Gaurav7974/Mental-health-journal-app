from flask import Blueprint, request, jsonify
from app.utils.decorators import jwt_required_user
from app.services.stt_service import convert_audio_to_text
from app.services.conversation_service import process_message
import tempfile

voice_bp = Blueprint("voice", __name__)

@voice_bp.route("/", methods=["POST"])
@jwt_required_user
def converse_voice(user_id):
    if "audio" not in request.files:
        return jsonify({"msg": "audio file required"}), 400

    file = request.files["audio"]

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        file.save(temp.name)
        text = convert_audio_to_text(temp.name)

    if not text:
        return jsonify({"msg": "speech processing failed"}), 500

    result = process_message(user_id, text)
    return jsonify(result), 200
