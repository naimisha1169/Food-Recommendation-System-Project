# Regional and Calorie-Based Food Recommendation System

A real-time, data-driven web application built with Flask that generates personalized Indian food recommendations based on user biometrics, activity levels, regional preferences, and dietary restrictions.

The application uses the **Mifflin-St Jeor Equation** to calculate a target calorie limit per meal and uses a **Weighted Penalty-Based Scoring Algorithm** to rank and recommend the best-matching dishes from a structured JSON dataset.


## Core Features

* **Biometric TDEE Calculator:** Automatically estimates daily energy expenditure and breaks it down to target meal metrics based on age, weight, gender, and activity factor.
* **Weighted Recommendation Engine:** Instead of using rigid "yes/no" database filters that often return zero results, the system calculates a mismatch penalty score to rank dishes, ensuring a "nearest best fit" fallback is always available.
* **Allergy Guard:** Implements a strict boolean safety filter that completely omits any dish containing user-specified allergens.
* **Regional & Dietary Segmentation:** Specifically tailored for Indian culinary contexts, organizing data across regions (North, South, East, West) and diet types (Veg, Non-Veg).
* **Serverless Deployment:** Structured to run efficiently on cloud platforms like Vercel using serverless functions.


## Technology Stack

* **Backend:** Python, Flask (WSGI Framework)
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Responsive Layout)
* **Data Layer:** Structured JSON (`dishes.json)
* **Deployment:** Vercel, GitHub (Continuous Integration)


## Project Structure

*├── app.py                 # Core Flask application & routing logic
*├── dishes.json            # Database containing dish metrics, regions, and allergens
*├── templates/
*│   ├── index.html         # User onboarding and biometric entry form
*│   └── results.html       # Dynamic recommendations and progress bar visualization
*├── requirements.txt       # Project dependencies
*└── vercel.json            # Serverless deployment configuration


## The Algorithm Explained

### 1. Calorie Target Generation

The system calculates the Basal Metabolic Rate (BMR) and adjusts it via an Activity Factor ($K$) to determine the Total Daily Energy Expenditure (TDEE). The single-meal target is calculated as:

  Meal Target = {BMR * k}/3


### 2. Penalty-Based Ranking

To rank dishes, the engine calculates a total score where **lower scores indicate a better match**:

  Score = |Dish Calories - Meal Target| + Penalties

* **Diet Type Mismatch:** $+1000$ penalty points.
* **Spice Level Exceeded:** $+500$ penalty points.
* **Region Mismatch:** $+200$ penalty points.
* *Note: If an item triggers an allergen match, it bypasses the scoring loop entirely and is omitted.*


## Data Architecture and Pipeline

The project operates as a lightweight data pipeline. While initial raw food metrics can be managed in flat CSV spreadsheets for easy manual data entry, the live application relies on a structured JSON format (`dishes.json`).

JSON is utilized over CSV in production because it supports nested arrays—allowing multiple allergens or ingredients to be tied to a single dish object—and parses natively into Python dictionaries for instant, real-time filtering when a user executes a search.
