from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import get_db_connection
from utils.meal_suggestions import get_meal_plan
from utils.meal_utils import get_calorie_limit
import traceback

app = Flask(__name__)
app.secret_key = 'supersecretkey'


# Home
@app.route('/')
def index():
    return render_template('index.html')

# about us
@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

#  contact us
@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')




# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        goal = request.form['goal']
        diet_type = request.form['diet_type']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, password, age, height, weight, goal, diet_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, email, password, age, height, weight, goal, diet_type))
            conn.commit()
            flash("Registration successful. Please login.")
            return redirect(url_for('login'))
        except Exception as e:
            print("Registration Error:", e)
            flash("Registration failed. Email may already exist.")
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


#  Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password.")

    return render_template('login.html')


#  Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute("SELECT goal FROM users WHERE id = %s", (user_id,))
    goal = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COALESCE(SUM(calories), 0)
        FROM meals
        WHERE user_id = %s AND date = CURDATE()
    """, (user_id,))
    calories_today = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COALESCE(SUM(hours), 0)
        FROM sleep_logs
        WHERE user_id = %s AND date = CURDATE()
    """, (user_id,))
    sleep_today = cursor.fetchone()[0]


    cursor.execute("""
        SELECT COALESCE(SUM(steps), 0)
        FROM step_logs
        WHERE user_id = %s AND date = CURDATE()
    """, (user_id,))
    steps_today = cursor.fetchone()[0]

    cursor.close()
    conn.close()


    from utils.meal_utils import get_calorie_limit
    calorie_limit = get_calorie_limit(goal)
    sleep_goal = 8
    step_goal = 8000

    return render_template(
        'dashboard.html',
        name=session['user_name'],
        calories_today=calories_today,
        calorie_limit=calorie_limit,
        sleep_today=sleep_today,
        sleep_goal=sleep_goal,
        steps_today=steps_today,
        step_goal=step_goal
    )


# Profile
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, email, age, height, weight, goal, diet_type
        FROM users WHERE id = %s
    """, (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("User profile not found.")
        return redirect(url_for('dashboard'))

    keys = ['name', 'email', 'age', 'height', 'weight', 'goal', 'diet_type']
    user_profile = dict(zip(keys, user))

    return render_template('profile.html', user=user_profile)

#  BMI Calculator
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    bmi = None
    category = ""

    if request.method == 'POST':
        try:
            height_cm = float(request.form['height'])
            weight_kg = float(request.form['weight'])
            height_m = height_cm / 100
            bmi = round(weight_kg / (height_m ** 2), 2)

            if bmi < 18.5:
                category = "Underweight"
            elif bmi < 24.9:
                category = "Normal weight"
            elif bmi < 29.9:
                category = "Overweight"
            else:
                category = "Obesity"

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_logs (user_id, bmi, date)
                VALUES (%s, %s, CURDATE())
            """, (session['user_id'], bmi))
            conn.commit()
            cursor.close()
            conn.close()
            flash(f"BMI calculated successfully!!","bmi")
        except Exception as e:
            print("BMI Error:", e)
            flash("Failed to calculate BMI. Try again.")

    return render_template('bmi.html', bmi=bmi, category=category,name=session['user_name'])


# Log Meal

@app.route('/log_meal', methods=['GET', 'POST'])
def log_meal():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        meal_time = request.form['meal_time']
        items = request.form['items']
        calories = int(request.form['calories'])

        conn = get_db_connection()
        cursor = conn.cursor()


        cursor.execute("""
            INSERT INTO meals (user_id, meal_time, items, calories, date)
            VALUES (%s, %s, %s, %s, CURDATE())
        """, (session['user_id'], meal_time, items, calories))
        conn.commit()

        cursor.execute("""
            SELECT SUM(calories) FROM meals
            WHERE user_id = %s AND date = CURDATE()
        """, (session['user_id'],))
        daily_total = cursor.fetchone()[0] or 0


        cursor.execute("SELECT goal FROM users WHERE id = %s", (session['user_id'],))
        goal = cursor.fetchone()[0]
        calorie_limit = get_calorie_limit(goal)

        cursor.close()
        conn.close()

        if daily_total > calorie_limit:
            flash(f"⚠️ You've exceeded your daily calorie limit of {calorie_limit} kcal! Today's total: {daily_total} kcal.","meal")
        else:
            flash(f"✅ You're within your daily calorie goal of {calorie_limit} kcal. Today's total: {daily_total} kcal.","meal")
        return redirect(url_for('dashboard'))

    return render_template('log_meal.html',name=session['user_name'])

# Log Sleep
@app.route('/log_sleep', methods=['GET', 'POST'])
def log_sleep():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        hours = float(request.form['hours'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sleep_logs (user_id, hours, date)
            VALUES (%s, %s, CURDATE())
        """, (session['user_id'], hours))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Sleep logged.","sleep")
        return redirect(url_for('dashboard'))

    return render_template('log_sleep.html')


# Log Steps
@app.route('/log_steps', methods=['GET', 'POST'])
def log_steps():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        steps = int(request.form['steps'])

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO step_logs (user_id, steps, date)
            VALUES (%s, %s, CURDATE())
        """, (session['user_id'], steps))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Steps logged.","steps")
        return redirect(url_for('dashboard'))

    return render_template('log_steps.html')


# Log Workout
@app.route('/log_workout', methods=['GET', 'POST'])
def log_workout():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        workout_type = request.form['type']
        duration = int(request.form['duration'])
        calories = duration * 6.0

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workout_logs (user_id, type, duration, calories_burned, date)
            VALUES (%s, %s, %s, %s, CURDATE())
        """, (session['user_id'], workout_type, duration, calories))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Workout logged.","workout")
        return redirect(url_for('dashboard'))

    return render_template('log_workout.html')

#  Meal Suggestions
@app.route('/meal_suggestions')
def meal_suggestions():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT age, goal, diet_type FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        flash("User not found.")
        return redirect(url_for('dashboard'))

    age, goal, diet_type = user

    try:
        meal_plan = get_meal_plan(age, goal, diet_type)
    except Exception as e:
        print("Meal plan error:", e)
        flash("Could not generate meal suggestions.")
        return redirect(url_for('dashboard'))

    return render_template('meal_suggestions.html', meal_plan=meal_plan, goal=goal, diet_type=diet_type)


# daily summary

@app.route('/daily_summary')
def daily_summary():

    if 'user_id' not in session:
        flash("Please login to view your daily summary.")
        return redirect(url_for('login'))

    user_id = session['user_id']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()


        cursor.execute("""
            SELECT items, calories FROM meals
            WHERE user_id = %s AND date = CURDATE()
        """, (user_id,))
        meals_data = cursor.fetchall() or []


        meals = [(item, cal) for item, cal in meals_data]


        total_calories_eaten = sum(cal for _, cal in meals) if meals else 0


        cursor.execute("""
            SELECT COALESCE(SUM(steps), 0) FROM step_logs
            WHERE user_id = %s AND date = CURDATE()
        """, (user_id,))
        total_steps = cursor.fetchone()[0] or 0


        calories_burned_steps = float(total_steps) * 0.04



        cursor.execute("""
            SELECT COALESCE(SUM(calories_burned), 0) FROM workout_logs
            WHERE user_id = %s AND date = CURDATE()
        """, (user_id,))
        calories_burned_workouts = cursor.fetchone()[0] or 0


        total_calories_burned = round(calories_burned_steps + calories_burned_workouts, 2)


        cursor.execute("""
            SELECT COALESCE(SUM(hours), 0) FROM sleep_logs
            WHERE user_id = %s AND date = CURDATE()
        """, (user_id,))
        total_sleep = cursor.fetchone()[0] or 0


        cursor.execute("""
            SELECT goal FROM users WHERE id = %s
        """, (user_id,))
        user_goal = cursor.fetchone()
        goal = user_goal[0] if user_goal else None

        cursor.close()
        conn.close()


        suggestions = []


        if total_sleep < 7:
            suggestions.append("Try to get at least 7 hours of sleep for better health.")


        if total_calories_eaten == 0 :
            suggestions.append("No calorie data recorded today. Make sure to log your meals.")
        elif total_calories_eaten > total_calories_burned:
            if goal == 'lose weight':
                suggestions.append("Your calorie intake is higher than calories burned. Consider adjusting your diet for weight loss.")
            elif goal == 'maintain weight':
                suggestions.append("Your calorie intake exceeds calories burned. Monitor to maintain your weight.")
            elif goal == 'gain muscle':
                suggestions.append("Calorie intake is higher than burned — good for muscle gain, but balance with workouts!")
        else:
            suggestions.append("Great job balancing your calories today!")
    except Exception as e:
        traceback.print_exc()
        flash(f"Oops! Could not load your daily summary: {e}")
        return redirect(url_for('dashboard'))


    return render_template(
    'daily_summary.html',
    name=session.get('user_name'),
    meals=meals,
    total_calories_eaten=total_calories_eaten,
    total_calories_burned=total_calories_burned,
    calories_burned_steps=round(calories_burned_steps, 2),
    calories_burned_workouts=round(calories_burned_workouts, 2),
    total_sleep=total_sleep,
    suggestions=suggestions
)



#  Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
