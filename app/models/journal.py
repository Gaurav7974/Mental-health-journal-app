from datetime import datetime
from bson import ObjectId
from app import db
from app.services.ml_service import analyze_journal  

class JournalModel:
    collection = db["journals"]

    @staticmethod
    def create(user_id, content):
        # Run AI Analysis
        analysis = analyze_journal(content)

        entry = {
            "user_id": user_id,
            "content": content,

            # AI Output
            "sentiment": analysis.get("sentiment"),
            "sentiment_score": analysis.get("sentiment_score"),
            "emotion": analysis.get("emotion"),
            "risk": analysis.get("risk"),

            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = JournalModel.collection.insert_one(entry)
        entry["_id"] = str(result.inserted_id)
        return entry

    @staticmethod
    def find_by_user(user_id):
        entries = JournalModel.collection.find({"user_id": user_id}).sort("created_at", -1)
        result = []
        for e in entries:
            e["_id"] = str(e["_id"])
            result.append(e)
        return result

    @staticmethod
    def update_entry(user_id, entry_id, content):
        return JournalModel.collection.update_one(
            {"_id": ObjectId(entry_id), "user_id": user_id},
            {"$set": {"content": content, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def delete_entry(user_id, entry_id):
        return JournalModel.collection.delete_one(
            {"_id": ObjectId(entry_id), "user_id": user_id}
        )
