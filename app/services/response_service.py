from app.services.llm_response_service import generate_llm_response

def generate_response(message, analysis, history=None):
    risk = analysis["risk"]

    # HARD SAFETY OVERRIDE — ALWAYS BACKEND CONTROL
    if risk == "severe":
        return (
            "I'm really glad you shared this with me. "
            "What you’re feeling matters and you don’t have to face it alone. "
            "If you feel unsafe, please reach your local emergency number immediately. "
            "If possible, reach someone you trust right now. You deserve real support and care.",
            True
        )

    # Moderate → LLM controlled (NO extra enforced English now)
    if risk == "moderate":
        reply = generate_llm_response(message, analysis, history)
        return reply, False

    # Normal → Full LLM response
    reply = generate_llm_response(message, analysis, history)
    return reply, False
