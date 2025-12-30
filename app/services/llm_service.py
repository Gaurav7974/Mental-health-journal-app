"""
LLM Service - Stage 1: Few-Shot Emotional Analysis
This replaces/updates your existing llm_service.py
"""

import os
from groq import Groq
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# Few-shot examples covering diverse emotional scenarios
FEW_SHOT_EXAMPLES = """
LEARN FROM THESE EXAMPLES:

EXAMPLE 1:
User: "Ex chhodh ke chale gayi ab lagta hai bas zinda nahi rehna"
Analysis: {
  "sentiment": "negative",
  "emotion": "heartbroken",
  "intensity": 10,
  "reason": "Breakup combined with suicidal ideation",
  "risk": "severe",
  "confidence": 0.95
}

EXAMPLE 2:
User: "Sab khatam ho gaya, koi raasta nahi bacha, I'm done"
Analysis: {
  "sentiment": "negative",
  "emotion": "overwhelmed",
  "intensity": 9,
  "reason": "Complete hopelessness with finality language",
  "risk": "severe",
  "confidence": 0.9
}

EXAMPLE 3:
User: "Job chali gayi, ghar waale naraz hain, ab kya karun"
Analysis: {
  "sentiment": "negative",
  "emotion": "anxious",
  "intensity": 7,
  "reason": "Multiple life stressors causing anxiety",
  "risk": "moderate",
  "confidence": 0.85
}

EXAMPLE 4:
User: "Bohot gussa aa raha hai manager pe, maar dunga ek din"
Analysis: {
  "sentiment": "negative",
  "emotion": "angry",
  "intensity": 8,
  "reason": "Extreme anger with violent ideation towards others",
  "risk": "moderate",
  "confidence": 0.8
}

EXAMPLE 5:
User: "Breakup ho gaya but I'll be fine, just need time"
Analysis: {
  "sentiment": "neutral",
  "emotion": "sad",
  "intensity": 5,
  "reason": "Processing breakup with healthy coping perspective",
  "risk": "none",
  "confidence": 0.8
}

EXAMPLE 6:
User: "Aj to bahut maza aaya, party mein full enjoy kiya"
Analysis: {
  "sentiment": "positive",
  "emotion": "happy",
  "intensity": 7,
  "reason": "Expressing joy from social gathering",
  "risk": "none",
  "confidence": 0.95
}

EXAMPLE 7:
User: "Roz ek hi baat, koi samajhta nahi, thak gaya hoon"
Analysis: {
  "sentiment": "negative",
  "emotion": "lonely",
  "intensity": 6,
  "reason": "Feeling chronically misunderstood and emotionally exhausted",
  "risk": "mild",
  "confidence": 0.75
}

EXAMPLE 8:
User: "Yaar sab theek nahi lag raha, panic attacks aa rahe hain"
Analysis: {
  "sentiment": "negative",
  "emotion": "anxious",
  "intensity": 8,
  "reason": "Experiencing panic attacks and general distress",
  "risk": "moderate",
  "confidence": 0.9
}

EXAMPLE 9:
User: "Maa baap ko disappoint kar diya, unke sapne tod diye"
Analysis: {
  "sentiment": "negative",
  "emotion": "guilty",
  "intensity": 7,
  "reason": "Feeling guilt over disappointing parents",
  "risk": "mild",
  "confidence": 0.85
}

EXAMPLE 10:
User: "Life mein kuch bhi achieve nahi kiya, worthless feel hota hai"
Analysis: {
  "sentiment": "negative",
  "emotion": "depressed",
  "intensity": 8,
  "reason": "Deep sense of worthlessness and lack of achievement",
  "risk": "moderate",
  "confidence": 0.85
}

NOW ANALYZE THE NEW MESSAGE BELOW.
"""

ANALYSIS_PROMPT = """
You are an expert emotional intelligence AI specializing in Indian languages and culture.

{few_shot_examples}

CRITICAL UNDERSTANDING:
- "zinda nahi rehna" = don't want to live → SEVERE risk
- "mar jaana" = want to die → SEVERE risk
- "khatam karna" = want to end it → SEVERE risk
- "sab khatam" = everything is over → Check for hopelessness
- "chhodh ke chale gaye" = abandoned/left → heartbroken/sad
- Hinglish, romanized Hindi, and code-switching MUST be understood
- Cultural context matters (family pressure, breakups, job loss)

JSON FORMAT (respond ONLY with this):
{{
  "sentiment": "positive | neutral | negative",
  "emotion": "sad | anxious | angry | happy | lonely | overwhelmed | confused | neutral | heartbroken | depressed | guilty | hopeless",
  "intensity": 1-10,
  "reason": "one sentence emotional summary",
  "risk": "none | mild | moderate | severe",
  "confidence": 0-1,
  "needs_deep_analysis": true/false
}}

RISK GUIDELINES:
- severe: Suicidal thoughts, self-harm intent, complete hopelessness
- moderate: Strong distress, harmful thoughts about others, crisis signs
- mild: Sadness, stress, normal life challenges
- none: Positive, neutral, or manageable emotions

Set "needs_deep_analysis": true if:
- Risk is moderate or severe
- Intensity is 8+
- Message is ambiguous but concerning
- Any mention of death, ending, giving up

User Message: "{text}"
"""

def analyze_emotion(text):
    """
    Stage 1: Broad emotional analysis with few-shot learning
    This is called by your main application
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert emotional analysis AI. You understand English, Hindi, Hinglish, and Indian cultural context perfectly. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(
                        few_shot_examples=FEW_SHOT_EXAMPLES,
                        text=text
                    )
                }
            ],
            temperature=0.7,
            max_tokens=800,
            response_format={"type": "json_object"}
        )

        # Parse the response
        text_response = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        parsed_data = json.loads(text_response)
        
        # Ensure needs_deep_analysis field exists
        if "needs_deep_analysis" not in parsed_data:
            # Auto-determine if deep analysis needed
            parsed_data["needs_deep_analysis"] = (
                parsed_data.get("risk") in ["moderate", "severe"] or
                parsed_data.get("intensity", 0) >= 8
            )
        
        return parsed_data

    except Exception as e:
        print(f"LLM Service Stage 1 Error: {e}")

        # fail-safe fallback with deep analysis flag set to true (safety first)
        return {
            "sentiment": "neutral",
            "emotion": "neutral",
            "intensity": 5,
            "reason": "Unable to analyze message clearly",
            "risk": "none",
            "confidence": 0.5,
            "needs_deep_analysis": True  # Trigger Stage 2 when uncertain
        }


# Keep backward compatibility if your code uses different function names
def analyze_text_with_model(text):
    """Alias for backward compatibility"""
    return analyze_emotion(text)