from app.services.conversation_service import process_message

def handle_conversation(user_id, message):
    try:
        response = process_message(user_id, message)
        return response, 200
    except Exception as e:
        print("Conversation Error:", e)
        return {"msg": "Something went wrong processing conversation"}, 500
