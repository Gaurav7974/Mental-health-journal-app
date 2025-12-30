from app import db

conversation_collection = db["conversations"]

def get_recent_context(user_id, limit=5):
    """
    Fetch last N user conversations in reverse time order
    """
    recent = list(conversation_collection
                  .find({"user_id": user_id})
                  .sort("created_at", -1)
                  .limit(limit))

    # reverse to chronological order
    recent.reverse()

    history = []
    for c in recent:
        history.append({
            "user_text": c.get("raw_text", ""),
            "emotion": c.get("analysis", {}).get("emotion", "unknown"),
            "intensity": c.get("analysis", {}).get("intensity", 5),
            "risk": c.get("analysis", {}).get("risk", "none"),
            "reply": c.get("reply", "")
        })

    return history
