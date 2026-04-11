from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load the processed food data
def load_data():
    if os.path.exists('dishes.json'):
        with open('dishes.json', 'r') as f:
            return json.load(f)
    return []

# Load data at startup
FOOD_DATA = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # 1. Capture Biometrics from Form
        age = int(request.form.get('age', 25))
        weight = int(request.form.get('weight', 70))
        gender = request.form.get('gender', 'male')
        activity = float(request.form.get('activity', 1.2))
        
        # 2. Capture Preferences & Spice
        pref_spice = int(request.form.get('spice', 5)) 
        pref_region = request.form.get('region', 'All')
        pref_diet = request.form.get('diet', 'All')
        user_allergies = request.form.getlist('allergies')

        # 3. AI Calorie Calculation (Mifflin-St Jeor Equation)
        if gender == "male":
            bmr = (10 * weight) + (6.25 * 170) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * 170) - (5 * age) - 161
        
        meal_target = (bmr * activity) / 3
        
        print(f"--- AI LOG ---")
        print(f"Targeting: {round(meal_target)} cal | Max Spice: {pref_spice}")

        recommendations = []
        for dish in FOOD_DATA:
            # CONSTRAINT 1: Allergy Check (This remains a HARD STOP for safety)
            if any(a in dish.get('allergies', []) for a in user_allergies):
                continue
            
            # --- WEIGHTED SCORING SYSTEM ---
            # We calculate a 'penalty' score. Lower score = Better match.
            
            # Start with the Calorie Difference as the base score
            score = abs(dish['cal'] - meal_target)
            
            # Penalty: Spice Level
            # If dish is spicier than user preference, add a heavy penalty
            dish_spice = int(dish.get('spice', 3))
            if dish_spice > pref_spice:
                score += 500  # Pushes spicy food to the bottom
            
            # Penalty: Diet Type
            # If user wants Veg but dish is Non-Veg, add a very heavy penalty
            if pref_diet != "All" and dish.get('diet') != pref_diet:
                score += 1000 
                
            # Penalty: Region
            if pref_region != "All" and dish.get('region') != pref_region:
                score += 200 

            # Add the score and metadata to the dish object for the template
            dish['match_score'] = score
            
            # Calculate progress bar percentage based on calorie target
            percent = (dish['cal'] / meal_target) * 100
            dish['percentage'] = min(round(percent, 1), 100)
            
            recommendations.append(dish)

        # 4. Final Sorting
        # We sort by 'match_score' (lowest penalty first)
        final_recs = sorted(recommendations, key=lambda x: x['match_score'])[:9]

        # Determine if we found exact matches or used a fallback
        # If the best match has a very high penalty, we know it's a fallback
        fallback_used = False
        if final_recs and final_recs[0]['match_score'] > 400:
            fallback_used = True

        return render_template('results.html', 
                               recs=final_recs, 
                               target=round(meal_target), 
                               fallback=fallback_used)

    except Exception as e:
        print(f"Error occurred: {e}")
        return "There was an error processing your request. Please check your inputs."

if __name__ == '__main__':
    app.run(debug=True)