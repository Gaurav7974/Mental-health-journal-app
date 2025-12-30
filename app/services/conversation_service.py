from datetime import datetime
from app import db
from app.services.llm_service import analyze_text_with_model
from app.services.response_service import generate_response
from app.services.validator_service import validate_analysis
from app.services.memory_service import get_recent_context

conversation_collection = db["conversations"]

def process_message(user_id, message):
    # Get structured emotional analysis from Gemini
    ai_raw = analyze_text_with_model(message)
    analysis = validate_analysis(ai_raw)
    conversation_history = get_recent_context(user_id)
    # Backend still controls safety & response
    reply, safe_mode = generate_response(message, analysis, conversation_history)

    # Save conversation
    entry = {
        "user_id": user_id,
        "raw_text": message,
        "analysis": analysis,
        "reply": reply,
        "safe_mode": safe_mode,
        "created_at": datetime.utcnow()
    }

    conversation_collection.insert_one(entry)

    # 4️⃣ Send back to client
    return {
        "analysis": analysis,
        "reply": reply,
        "safe_mode": safe_mode
    }
