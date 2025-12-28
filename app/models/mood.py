from datetime import datetime
from app import db

class MoodModel:
    collection = db["moods"]

    @staticmethod
    def log(user_id, mood_score, emotion=None, note=None):
        entry = {
            "user_id": user_id,
            "mood_score": mood_score,   # 1 - 10
            "emotion": emotion,         # angry / sad / happy / anxious / neutral etc
            "note": note,
            "created_at": datetime.utcnow()
        }
        MoodModel.collection.insert_one(entry)
        entry["_id"] = str(entry["_id"])
        return entry

    @staticmethod
    def get_history(user_id):
        moods = MoodModel.collection.find({"user_id": user_id}).sort("created_at", -1)
        result = []
        for m in moods:
            m["_id"] = str(m["_id"])
            result.append(m)
        return result

    @staticmethod
    def get_stats(user_id):
        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$group": {
                    "_id": None,
                    "avg_mood": {"$avg": "$mood_score"},
                    "count": {"$sum": 1}
                }
            }
        ]
        result = list(MoodModel.collection.aggregate(pipeline))
        return result[0] if result else {"avg_mood": 0, "count": 0}
