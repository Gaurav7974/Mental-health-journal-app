from flask import Blueprint, request, jsonify
from app.controllers.journal_controller import (
    create_journal_entry,
    get_user_journals,
    update_journal_entry,
    delete_journal_entry
)
from app.utils.decorators import jwt_required_user

journal_bp = Blueprint("journal", __name__)

@journal_bp.route("/", methods=["POST"])
@jwt_required_user
def create(user_id):
    data = request.json
    result, code = create_journal_entry(user_id, data)
    return jsonify(result), code


@journal_bp.route("/", methods=["GET"])
@jwt_required_user
def get_all(user_id):
    result, code = get_user_journals(user_id)
    return jsonify(result), code


@journal_bp.route("/<entry_id>", methods=["PUT"])
@jwt_required_user
def update(user_id, entry_id):
    data = request.json
    result, code = update_journal_entry(user_id, entry_id, data)
    return jsonify(result), code


@journal_bp.route("/<entry_id>", methods=["DELETE"])
@jwt_required_user
def delete(user_id, entry_id):
    result, code = delete_journal_entry(user_id, entry_id)
    return jsonify(result), code
