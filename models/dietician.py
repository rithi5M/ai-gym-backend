from typing import Dict

def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h*h), 2)

def maintenance_calories(weight):
    return int(weight * 30)

def get_goal_calories(maint, goal):
    g = goal.lower()
    if "loss" in g: return maint - 400
    if "gain" in g or "muscle" in g: return maint + 300
    return maint

def generate_diet_plan(weight, height, age, goal, pref) -> Dict:
    bmi = calculate_bmi(weight, height)
    maint = maintenance_calories(weight)
    target = get_goal_calories(maint, goal)

    if "veg" in pref.lower():
        diet = {
            "breakfast": "Oats + banana",
            "lunch": "Brown rice + dal + veggies",
            "dinner": "Roti + paneer",
            "snacks": "Fruits + nuts"
        }
    else:
        diet = {
            "breakfast": "Egg omelette + fruit",
            "lunch": "Rice + chicken + veggies",
            "dinner": "Roti + chicken curry",
            "snacks": "Boiled eggs + yogurt"
        }

    return {
        "bmi": bmi,
        "maintenance_calories": maint,
        "target_calories": target,
        "plan": diet
    }
