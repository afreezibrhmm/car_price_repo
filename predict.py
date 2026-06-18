import pandas as pd
import joblib

# 1. Load the trained pipeline
print("Loading model...")
model = joblib.load("car_price_model.pkl")

# 2. Define a "new" car (This mimics what a user would enter on a website)
new_car_data = {
    "brand": ["Porsche"],
    "model": ["911 Carrera S"],
    "model_year": [2019],
    "milage": ["15,000 mi."], 
    "fuel_type": ["Gasoline"],
    "engine": ["420.0HP 3.0L Flat 6 Cylinder Engine Gasoline Fuel"],
    "transmission": ["7-Speed A/T"],
    "ext_col": ["White"],
    "int_col": ["Black"],
    "accident": ["None reported"],
    "clean_title": ["Yes"]
}

df_new = pd.DataFrame(new_car_data)

# 3. Apply the exact same cleaning steps used in training
# Clean Milage
df_new['milage'] = df_new['milage'].astype(str).str.replace(' mi.', '', regex=False)
df_new['milage'] = df_new['milage'].str.replace(',', '', regex=False)
df_new['milage'] = pd.to_numeric(df_new['milage'], errors='coerce')

# Calculate Age
df_new['car_age'] = 2026 - df_new['model_year']

# Extract Engine details
df_new['engine'] = df_new['engine'].astype(str)
df_new['horsepower'] = df_new['engine'].str.extract(r'(\d+\.?\d*)\s*HP').astype(float)
df_new['engine_displacement_liters'] = df_new['engine'].str.extract(r'(\d+\.?\d*)\s*L').astype(float)

# 4. Make the Prediction
predicted_price = model.predict(df_new)[0]

print("\n--- Prediction Result ---")
print(f"Vehicle: {new_car_data['model_year'][0]} {new_car_data['brand'][0]} {new_car_data['model'][0]}")
print(f"Estimated Value: ${predicted_price:,.2f}")