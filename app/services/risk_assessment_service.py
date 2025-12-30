"""
Risk Assessment Service - Stage 2: Deep Risk Analysis
NEW FILE - Add this to your services folder
"""

import os
from groq import Groq
import json

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

RISK_ASSESSMENT_PROMPT = """
You are a specialized crisis detection and risk assessment expert.

Your ONLY job is to accurately assess self-harm and suicide risk.

CONTEXT FROM STAGE 1:
- User's message: "{text}"
- Detected emotion: {emotion}
- Intensity: {intensity}/10
- Initial risk: {initial_risk}

DEEP RISK ANALYSIS FRAMEWORK:

1. DIRECT INDICATORS (Highest Priority):
   - Explicit statements about death/dying/suicide
   - "zinda nahi rehna", "mar jaana", "khatam karna"
   - "I want to die", "kill myself", "end it all"
   - Any language expressing desire to not exist

2. INDIRECT INDICATORS (High Priority):
   - Complete hopelessness ("no way out", "sab khatam")
   - Finality language ("everything is over", "nothing left")
   - Loss of future perspective (no mention of tomorrow/plans)
   - Feeling like a burden ("everyone would be better without me")
   - Giving up statements ("I'm done", "can't do this anymore")

3. CONTEXTUAL FACTORS:
   - Recent major loss (breakup, job, death)
   - Social isolation ("no one understands", "alone")
   - Accumulated stressors (multiple problems)
   - Expression of pain with no coping mentioned

4. PROTECTIVE FACTORS (Risk Reducers):
   - Mention of support system (friends, family)
   - Future plans or goals mentioned
   - Seeking help behavior (talking about it)
   - Coping mechanisms mentioned
   - Humor or resilience indicators

5. LINGUISTIC CUES:
   - Hinglish expressions of finality
   - Code-switching intensity (more English = more serious?)
   - Repetition of negative themes
   - Absolutist language ("always", "never", "everything")

RISK CLASSIFICATION:

SEVERE = Immediate danger
- Clear suicidal ideation
- Specific plan or method mentioned
- Complete hopelessness with no protective factors
- "I'm going to..." statements

MODERATE = Elevated concern
- Passive death wishes ("wish I wasn't here")
- Strong hopelessness but some protective factors
- Harmful thoughts without immediate plan
- Crisis state but still reaching out

MILD = Some concern
- Emotional distress without death ideation
- Temporary hopelessness with coping present
- Life stressors causing pain but manageable

NONE = No immediate concern
- Normal sadness/stress responses
- Protective factors present
- Future-oriented thinking
- Seeking support healthily

Respond ONLY with JSON:
{{
  "risk": "none | mild | moderate | severe",
  "risk_confidence": 0-1,
  "risk_reasoning": "detailed explanation of risk assessment",
  "protective_factors": ["list", "of", "any", "protective", "factors"],
  "warning_signs": ["list", "of", "concerning", "indicators"],
  "recommended_action": "immediate_crisis | professional_help | supportive_monitoring | general_support"
}}
"""

def assess_risk_deeply(text, stage1_analysis):
    """
    Stage 2: Specialized deep risk assessment
    Only called when Stage 1 flags needs_deep_analysis
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a crisis detection specialist. Your assessments can save lives. Be thorough, cautious, and err on the side of safety. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": RISK_ASSESSMENT_PROMPT.format(
                        text=text,
                        emotion=stage1_analysis.get('emotion', 'unknown'),
                        intensity=stage1_analysis.get('intensity', 0),
                        initial_risk=stage1_analysis.get('risk', 'unknown')
                    )
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent risk assessment
            max_tokens=1000,
            response_format={"type": "json_object"}
        )

        # Parse the response
        text_response = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        risk_data = json.loads(text_response)
        
        return risk_data

    except Exception as e:
        print(f"Risk Assessment Service Error: {e}")

        # Safety-first fallback: if Stage 2 fails, escalate risk
        return {
            "risk": "moderate",  # Assume moderate if we can't assess
            "risk_confidence": 0.5,
            "risk_reasoning": "Unable to complete deep risk assessment - escalating for safety",
            "protective_factors": [],
            "warning_signs": ["Unable to analyze properly"],
            "recommended_action": "professional_help"
        }


def merge_analyses(stage1, stage2):
    """
    Merge Stage 1 and Stage 2 results intelligently
    Takes the HIGHER risk level (safety first)
    """
    
    # Take the HIGHER risk level (safety first)
    risk_levels = ['none', 'mild', 'moderate', 'severe']
    stage1_risk_index = risk_levels.index(stage1.get('risk', 'none'))
    stage2_risk_index = risk_levels.index(stage2.get('risk', 'none'))
    
    final_risk = risk_levels[max(stage1_risk_index, stage2_risk_index)]
    
    # Merge into comprehensive analysis
    merged = {
        "sentiment": stage1.get("sentiment"),
        "emotion": stage1.get("emotion"),
        "intensity": stage1.get("intensity"),
        "reason": stage1.get("reason"),
        "risk": final_risk,
        "confidence": (stage1.get("confidence", 0) + stage2.get("risk_confidence", 0)) / 2,
        
        # Stage 2 specific fields
        "risk_reasoning": stage2.get("risk_reasoning"),
        "protective_factors": stage2.get("protective_factors", []),
        "warning_signs": stage2.get("warning_signs", []),
        "recommended_action": stage2.get("recommended_action"),
        
        # Metadata
        "deep_analysis_performed": True
    }
    
    return merged