# utils/meal_utils.py

def get_calorie_limit(goal):
    goal = goal.lower()
    if goal == "lose weight":
        return 1800
    elif goal == "maintain weight":
        return 2200
    elif goal == "gain muscle":
        return 2600
    else:
        return 2000


