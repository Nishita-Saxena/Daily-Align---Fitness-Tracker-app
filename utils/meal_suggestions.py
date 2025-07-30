def get_meal_plan(age, goal, diet_type):
    # Example plans — you can expand later
    indian_meals = {
    "Lose Weight": {
        "Vegetarian": {
            "Breakfast": "Oats with fruits and green tea",
            "Lunch": "1 roti, sabzi (low oil), salad, dal",
            "Dinner": "Quinoa khichdi, curd, steamed veggies"
        },
        "Vegan": {
            "Breakfast": "Chia pudding with almond milk",
            "Lunch": "Brown rice, rajma, salad",
            "Dinner": "Vegetable stir fry, tofu tikka"
        },
        "Non-Veg": {
            "Breakfast": "Boiled eggs, apple",
            "Lunch": "Grilled fish, steamed veggies, brown rice",
            "Dinner": "Chicken salad, soup"
        },
        "Keto": {
            "Breakfast": "Paneer bhurji, green tea",
            "Lunch": "Grilled chicken, avocado salad",
            "Dinner": "Zucchini noodles with egg and cheese"
        },
        "No Preference": {
            "Breakfast": "Boiled eggs, poha",
            "Lunch": "Grilled chicken, roti, salad",
            "Dinner": "Fish curry, brown rice, sautéed veggies"
        }
    },
    "Gain Muscle": {
        "Vegetarian": {
            "Breakfast": "Paneer sandwich, banana, milk",
            "Lunch": "2 rotis, dal, sabzi, salad, curd",
            "Dinner": "Soyabean curry, rice, curd"
        },
        "Vegan": {
            "Breakfast": "Tofu scramble, oats",
            "Lunch": "Lentil curry, brown rice, salad",
            "Dinner": "Chickpea salad, rice, almond milk"
        },
        "Non-Veg": {
            "Breakfast": "Omelette, toast, banana",
            "Lunch": "Chicken curry, rice, boiled eggs",
            "Dinner": "Grilled fish, quinoa, curd"
        },
        "Keto": {
            "Breakfast": "Scrambled eggs with spinach",
            "Lunch": "Lamb kebabs, mixed greens with olive oil",
            "Dinner": "Egg curry with cauliflower rice"
        },
        "No Preference": {
            "Breakfast": "Egg bhurji, toast",
            "Lunch": "Chicken curry, rice, boiled eggs",
            "Dinner": "Mutton stew, chapati"
        }
    },
    "Maintain Weight": {
        "Vegetarian": {
            "Breakfast": "Idli with sambar, fruit",
            "Lunch": "Roti, sabzi, dal, salad",
            "Dinner": "Moong dal dosa, chutney, veggies"
        },
        "Vegan": {
            "Breakfast": "Smoothie bowl",
            "Lunch": "Veg biryani with raita (vegan)",
            "Dinner": "Bajra roti, sabzi"
        },
        "Non-Veg": {
            "Breakfast": "Boiled eggs, upma",
            "Lunch": "Fish curry, rice",
            "Dinner": "Chicken soup, roti"
        },
        "Keto": {
            "Breakfast": "Avocado and egg salad",
            "Lunch": "Paneer tikka with salad",
            "Dinner": "Grilled chicken with sautéed greens"
        },
        "No Preference": {
            "Breakfast": "Eggs, upma",
            "Lunch": "Fish curry, rice",
            "Dinner": "Dal, roti, salad"
        }
    }
}

    goal_plan = indian_meals.get(goal)
    if not goal_plan:
        return {"error": "No plan for goal"}

    diet_plan = goal_plan.get(diet_type)
    if not diet_plan:
        diet_plan = goal_plan.get("No Preference")

    return diet_plan
