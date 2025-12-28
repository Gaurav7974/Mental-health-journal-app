from app.models.mood import MoodModel

def log_mood(user_id, data):
    if "mood_score" not in data:
        return {"msg": "mood_score required"}, 400

    score = data["mood_score"]

    if not isinstance(score, int) or score < 1 or score > 10:
        return {"msg": "mood_score must be integer 1-10"}, 400

    emotion = data.get("emotion")
    note = data.get("note")

    entry = MoodModel.log(user_id, score, emotion, note)

    return {"msg": "Mood logged", "entry": entry}, 201


def get_mood_history(user_id):
    history = MoodModel.get_history(user_id)
    return {"history": history}, 200


def get_mood_stats(user_id):
    stats = MoodModel.get_stats(user_id)
    return {"stats": stats}, 200
