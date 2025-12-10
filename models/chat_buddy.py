def analyze_sentiment(text):
    t = text.lower()
    neg = ["tired", "sad", "lazy", "skip"]
    pos = ["great", "good", "happy", "excited"]

    if any(w in t for w in neg): return "negative"
    if any(w in t for w in pos): return "positive"
    return "neutral"

def reply_to_user(text):
    s = analyze_sentiment(text)

    if s == "negative":
        msg = "It's okay to feel low. Try a light 10-minute workout today!"
    elif s == "positive":
        msg = "Awesome energy! Push yourself a little extra today 💪"
    else:
        msg = "Let's keep going! Tell me your goal for this week."

    return {"sentiment": s, "reply": msg}
