from flask import Blueprint, jsonify
from app.utils.decorators import jwt_required_user
from app.controllers.insights_controller import (
    get_overview_insights,
    get_emotion_trend,
    get_risk_summary
)

insights_bp = Blueprint("insights", __name__)

@insights_bp.route("/overview", methods=["GET"])
@jwt_required_user
def overview(user_id):
    data = get_overview_insights(user_id)
    return jsonify(data), 200


@insights_bp.route("/emotion-trend", methods=["GET"])
@jwt_required_user
def emotion(user_id):
    data = get_emotion_trend(user_id)
    return jsonify(data), 200


@insights_bp.route("/risk-summary", methods=["GET"])
@jwt_required_user
def risk(user_id):
    data = get_risk_summary(user_id)
    return jsonify(data), 200
