import os
import requests
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_llm_response(message, analysis, history=None):
    try:
        emotion = analysis.get("emotion", "neutral")
        intensity = analysis.get("intensity", 5)
        risk = analysis.get("risk", "none")
        reason = analysis.get("reason", "")

        # -------------------------
        # 🧠 Build Conversation Memory Text
        # -------------------------
        history_text = ""
        if history and len(history) > 0:
            history_text = "Recent Emotional Context:\n"
            for h in history:
                history_text += (
                    f"- User said: {h.get('user_text','')} | "
                    f"Emotion: {h.get('emotion','unknown')} | "
                    f"Intensity: {h.get('intensity',5)} | "
                    f"Risk: {h.get('risk','none')}\n"
                )

        # -------------------------
        # 🌟 Base Core Personality
        # -------------------------
        system_message = (
            "You are a warm, calm, emotionally supportive companion. "
            "Respond like a caring Indian friend, not a therapist or textbook. "
            "Use natural Hinglish if user uses Hinglish. Otherwise use English. "
            "Be empathetic, human, conversational. "
            "Avoid lecture tone. Avoid robotic Hindi. Avoid clinical counseling. "
            "Never guilt-trip, shame, or judge. "
            "Do not diagnose or claim to be a professional. "
            "Be culturally aware: Indian work stress, studies, relationships, family pressure. "
            "Always reply ONLY in JSON."
        )

        # -------------------------
        # 🎚️ Intensity Adaptive Tone
        # -------------------------
        tone_context = ""
        if intensity <= 3:
            tone_context = (
                "Tone Requirement: Very gentle reassurance, light emotional support, "
                "encourage simple sharing."
            )
        elif 4 <= intensity <= 7:
            tone_context = (
                "Tone Requirement: Stronger empathy, acknowledge emotional weight, "
                "include one simple practical suggestion."
            )
        else:
            tone_context = (
                "Tone Requirement: Deep emotional comfort. Very soft tone. "
                "Avoid advice tone. Focus on presence & grounding reassurance."
            )

        # -------------------------
        # 🤖 Domain Restriction
        # -------------------------
        domain_rule = (
            "If the user asks unrelated questions like coding, math, facts, general chat "
            "— gently refuse and say: "
            "\"I'm here to support your emotional wellbeing. Agar chahein to apni feelings share karo.\""
        )

        # -------------------------
        # ⚠️ Risk Context Tone
        # -------------------------
        risk_context = ""
        if risk == "mild":
            risk_context = (
                "User feels discomfort but not in danger. Be soothing, supportive, friendly."
            )
        elif risk == "moderate":
            risk_context = (
                "User is emotionally struggling. Be compassionate. "
                "Encourage talking to a trusted person gently."
            )
        elif risk == "severe":
            risk_context = (
                "If risk = severe, do NOT casually chat. "
                "Be emotionally supportive and encourage real world help."
            )

        # -------------------------
        # 🎭 Adaptive Emotional Personality
        # -------------------------
        auto_personality_context = ""

        if emotion in ["sad", "lonely", "hurt"]:
            auto_personality_context = (
                "Personality: Very warm, slow, emotionally comforting, validating feelings. "
                "Avoid advice tone. Focus on emotional support."
            )

        elif emotion in ["anxious", "stressed", "overwhelmed"]:
            auto_personality_context = (
                "Personality: Calm, grounding, reassuring. "
                "Help the user mentally slow down and feel safe. "
                "One gentle practical suggestion allowed."
            )

        elif emotion in ["angry", "frustrated"]:
            auto_personality_context = (
                "Personality: Non-judgmental, stabilizing, acknowledging frustration. "
                "Do NOT say 'calm down'. No moral lecture."
            )

        elif emotion in ["happy", "relieved"]:
            auto_personality_context = (
                "Personality: Light, positive, encouraging but not cheesy."
            )

        else:
            auto_personality_context = (
                "Personality: Warm, supportive friend tone with emotional awareness."
            )

        # -------------------------
        # 🧠 Final Prompt
        # -------------------------
        prompt = f"""
{tone_context}

{domain_rule}

Risk Context:
{risk_context}

Adaptive Personality Context:
{auto_personality_context}

{history_text}

Current Message:
"{message}"

Emotion: {emotion}
Intensity: {intensity}/10
Risk: {risk}
Reason: {reason}

OUTPUT FORMAT STRICT:
Return ONLY JSON:
{{
 "reply": "empathetic human response"
}}
"""

        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(GROQ_URL, headers=headers, json=payload)
        response.raise_for_status()

        raw_text = response.json()["choices"][0]["message"]["content"]

        # -------------------------
        # 🛡️ JSON Extraction
        # -------------------------
        try:
            start = raw_text.index("{")
            end = raw_text.rindex("}") + 1
            parsed = json.loads(raw_text[start:end])
            return parsed.get("reply")

        except Exception:
            print("Reply JSON extraction failed. Raw:", raw_text)
            return (
                "I'm here with you. You're not alone in this. "
                "Agar theek lage to thoda aur share karo jo feel ho raha hai."
            )

    except Exception as e:
        print("Groq Reply Error:", e)
        return (
            "I'm right here with you. "
            "You don't have to face everything alone."
        )
