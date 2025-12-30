def validate_analysis(raw):
    """
    Ensures AI emotional JSON is always safe, valid, and predictable.
    If something is missing → auto-correct
    If nonsense → fallback safe defaults
    """

    SAFE_DEFAULT = {
        "sentiment": "neutral",
        "emotion": "neutral",
        "intensity": 5,
        "reason": "not clearly understood",
        "risk": "none",
        "confidence": 0.5
    }

    try:
        sentiment = raw.get("sentiment", "neutral")
        emotion = raw.get("emotion", "neutral")
        intensity = raw.get("intensity", 5)
        reason = raw.get("reason", "not clearly understood")
        risk = raw.get("risk", "none")
        confidence = raw.get("confidence", 0.5)

        # normalize intensity
        if not isinstance(intensity, int):
            try:
                intensity = int(float(intensity))
            except:
                intensity = 5

        intensity = max(1, min(intensity, 10))

        # normalize risk
        VALID_RISKS = ["none", "mild", "moderate", "severe"]
        if risk not in VALID_RISKS:
            risk = "none"

        # auto safety override
        text = (raw.get("reason", "") + " " + raw.get("emotion", "")).lower()

        danger_words = ["die", "suicide", "kill", "worthless", "self harm"]
        if any(word in text for word in danger_words):
            risk = "severe"
            confidence = max(confidence, 0.9)

        return {
            "sentiment": sentiment,
            "emotion": emotion,
            "intensity": intensity,
            "reason": reason,
            "risk": risk,
            "confidence": confidence
        }

    except Exception as e:
        print("Validator failed, using fallback", e)
        return SAFE_DEFAULT
