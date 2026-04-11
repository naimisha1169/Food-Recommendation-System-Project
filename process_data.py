import pandas as pd
import json
import os

def guess_spice_level(food_name):
    """
    Categorizes Indian dishes into 5 spice levels based on common culinary keywords.
    """
    name = str(food_name).lower()
    
    # LEVEL 1: Neutral / Sweet / Cooling (The 'Safe' Zone)
    if any(word in name for word in [
        'dahi', 'curd', 'sweet', 'kheer', 'payasam', 'dessert', 'halwa', 'milk', 
        'boiled', 'plain', 'steamed', 'idli', 'upma', 'poha', 'banana', 'coconut milk', 
        'malai', 'korma', 'custard', 'lassi', 'misti', 'sandesh', 'white rice', 'sugar'
    ]):
        return 1
    
    # LEVEL 5: Fiery / High Heat
    if any(word in name for word in [
        'chili', 'mirch', 'kolhapuri', 'vindaloo', 'schezwan', 'andhra', 'chettinad', 
        'jhal', 'teekha', 'bhuna', 'kadhai', 'kadai', 'hot', 'peri peri', 'peppercorn'
    ]):
        return 5
    
    # LEVEL 4: Spicy / Masala Heavy
    if any(word in name for word in [
        'masala', 'biryani', 'tikka', 'curry', 'tandoori', 'jalfrezi', 'balti', 
        'rogan josh', 'sambar', 'vada pav', 'samosa', 'chaat', 'manchurian', 'achar'
    ]):
        return 4
    
    # LEVEL 2: Mild Savory / Comfort Food
    if any(word in name for word in [
        'dal tadka', 'moong', 'khichdi', 'roti', 'naan', 'paratha', 'saag', 
        'palak', 'stew', 'soup', 'bread', 'papad', 'dhokla', 'dosa'
    ]):
        return 2
        
    # LEVEL 3: Standard Indian Medium (Default)
    return 3

def process_nutrition_data(input_csv):
    if not os.path.exists(input_csv):
        print(f"Error: {input_csv} not found!")
        return

    # Read the CSV
    df = pd.read_csv(input_csv)

    processed_dishes = []

    for index, row in df.iterrows():
        try:
            food_name = str(row['Food_Name']).strip()
            
            # Nutrition Mapping (with float safety)
            calories = int(float(row['Calories (kcal)']))
            protein = int(float(row['Protein (g)']))
            fats = int(float(row['Fats (g)']))
            fiber = int(float(row['Fibre (g)']))
            
            # Skip entries with 0 calories to avoid corrupting recommendations
            if calories <= 0:
                continue

            # 1. Base Dish Object
            dish = {
                "name": food_name,
                "cal": calories,
                "p": protein,
                "f": fats,
                "fib": fiber,
                "spice": guess_spice_level(food_name),
                "region": "All", # Defaulting to 'All' to match your app logic
                "diet": "Vegetarian", # Default to Veg
                "allergies": []
            }
            
            # 2. Diet Tagging
            # Check for meat keywords
            if any(word in food_name.lower() for word in ['chicken', 'mutton', 'fish', 'egg', 'meat', 'pork', 'beef', 'prawn']):
                dish['diet'] = 'Non-Vegetarian'
            
            # 3. Allergy Tagging
            # Detect Dairy
            if any(word in food_name.lower() for word in ['milk', 'paneer', 'curd', 'cheese', 'ghee', 'cream', 'butter', 'dahi']):
                dish['allergies'].append('Dairy')
            
            # Detect Nuts (Common in Indian sweets/curries)
            if any(word in food_name.lower() for word in ['almond', 'cashew', 'peanut', 'kaju', 'badam', 'walnut']):
                dish['allergies'].append('Nuts')

            processed_dishes.append(dish)

        except Exception as e:
            # Logs the error but keeps processing the rest of the file
            print(f"Skipping row {index} due to error: {e}")
            continue

    # Save to JSON
    with open('dishes.json', 'w') as f:
        json.dump(processed_dishes, f, indent=4)
    
    print(f"--- SUCCESS ---")
    print(f"Processed {len(processed_dishes)} dishes.")
    print(f"File saved as: dishes.json")

if __name__ == "__main__":
    process_nutrition_data('Indian_Food_Nutrition_Processed.csv')