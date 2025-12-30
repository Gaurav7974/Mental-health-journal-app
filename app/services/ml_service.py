from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer

# Import hybrid analysis components - 
from app.services.llm_service import analyze_emotion as llm_analyze_emotion
from app.services.risk_assessment_service import assess_risk_deeply, merge_analyses

sia = SentimentIntensityAnalyzer()

RISK_KEYWORDS = [
    "suicide", "kill myself", "end my life",
    "i want to die", "i don't want to live",
    "self harm", "cut myself", "hopeless",
    "worthless", "no point in living"
]


def analyze_sentiment(text):
    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score >= 0.4:
        sentiment = "positive"
    elif sentiment_score <= -0.4:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return sentiment, float(sentiment_score)


def analyze_emotion(text):
    text_lower = text.lower()

    if "anxious" in text_lower or "worried" in text_lower or "stress" in text_lower:
        return "anxious"
    if "sad" in text_lower or "cry" in text_lower or "lonely" in text_lower:
        return "sad"
    if "angry" in text_lower or "mad" in text_lower or "frustrated" in text_lower:
        return "angry"
    if "happy" in text_lower or "grateful" in text_lower or "good" in text_lower:
        return "happy"

    return "neutral"


def detect_risk(text):
    text_lower = text.lower()
    for word in RISK_KEYWORDS:
        if word in text_lower:
            return True
    return False


def analyze_journal(text):
    """Legacy function - kept for backward compatibility"""
    sentiment, sentiment_score = analyze_sentiment(text)
    emotion = analyze_emotion(text)
    risk = detect_risk(text)

    return {
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "emotion": emotion,
        "risk": risk
    }


# NEW HYBRID ANALYSIS FUNCTIONS

def analyze_message_hybrid(text):
    """
    Main hybrid analysis function using LLM-based two-stage approach
    Use this for chatbot messages
    """
    # STAGE 1: Few-Shot Emotional Analysis
    print("🔍 Stage 1: Analyzing emotions with LLM...")
    stage1_result = llm_analyze_emotion(text)
    
    # Check if deep analysis is needed
    needs_deep_check = stage1_result.get("needs_deep_analysis", False)
    
    # STAGE 2: Deep Risk Assessment (conditional)
    if needs_deep_check:
        print("⚠️  Stage 2: Deep risk assessment triggered...")
        stage2_result = assess_risk_deeply(text, stage1_result)
        
        # Merge both analyses
        final_result = merge_analyses(stage1_result, stage2_result)
        print("✅ Two-stage analysis complete")
        
    else:
        # Stage 1 was sufficient
        final_result = stage1_result
        final_result["deep_analysis_performed"] = False
        print("✅ Stage 1 analysis sufficient")
    
    return final_result


def get_safe_mode_status(analysis):
    """Determine if safe mode should be activated"""
    risk = analysis.get("risk", "none")
    return risk in ["severe", "moderate"]