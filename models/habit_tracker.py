from datetime import datetime, date

habit_logs = []

def log_workout_entry(did, mood):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "date": str(date.today()),
        "did_workout": did,
        "mood": mood.lower()
    }
    habit_logs.append(entry)
    return entry

def get_summary():
    total = len(habit_logs)
    done = sum(1 for x in habit_logs if x["did_workout"])
    skipped = total - done
    rate = round(done / total * 100, 2) if total else 0

    return {
        "total_days_logged": total,
        "workouts_done": done,
        "workouts_skipped": skipped,
        "completion_rate_percent": rate,
        "logs": habit_logs[-10:]
    }

def predict_skip_risk():
    summary = get_summary()
    rate = summary["completion_rate_percent"]
    mood = habit_logs[-1]["mood"] if habit_logs else "unknown"

    if rate < 50 or mood in ["sad", "tired", "lazy"]:
        return {"risk": "high", "coach_message": "You may skip your next workout."}
    
    return {"risk": "low", "coach_message": "Great consistency!"}
