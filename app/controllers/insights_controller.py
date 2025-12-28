from app.models.journal import JournalModel
from app.models.mood import MoodModel
from app import db

def get_overview_insights(user_id):
    journals = list(db["journals"].find({"user_id": user_id}))
    conversations = list(db["conversations"].find({"user_id": user_id}))
    moods = list(db["moods"].find({"user_id": user_id}))

    total_entries = len(journals)
    total_conversations = len(conversations)
    total_moods = len(moods)

    negative_count = sum(1 for j in journals if j.get("sentiment") == "negative")
    positive_count = sum(1 for j in journals if j.get("sentiment") == "positive")

    severe_risk = sum(1 for c in conversations if c.get("analysis", {}).get("risk") == "severe")

    return {
        "total_journals": total_entries,
        "total_conversations": total_conversations,
        "total_mood_logs": total_moods,
        "positive_journals": positive_count,
        "negative_journals": negative_count,
        "risk_flags": severe_risk
    }


def get_emotion_trend(user_id):
    conversations = list(db["conversations"].find({"user_id": user_id}).sort("created_at", -1).limit(20))

    trend = [
        {
            "time": str(c["created_at"]),
            "emotion": c["analysis"]["emotion"],
            "intensity": c["analysis"]["intensity"]
        }
        for c in conversations
    ]

    return {"trend": list(reversed(trend))}


def get_risk_summary(user_id):
    conversations = list(db["conversations"].find({"user_id": user_id}))

    none = mild = moderate = severe = 0

    for c in conversations:
        risk = c.get("analysis", {}).get("risk", "none")
        if risk == "none":
            none += 1
        elif risk == "mild":
            mild += 1
        elif risk == "moderate":
            moderate += 1
        elif risk == "severe":
            severe += 1

    return {
        "none": none,
        "mild": mild,
        "moderate": moderate,
        "severe": severe
    }
