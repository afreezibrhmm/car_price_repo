import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# 1. Load Data
df = pd.read_csv("car_price_prediction_.csv")

# Clean up any accidental whitespaces in column names
df.columns = df.columns.str.strip()

# --- STEP 2: DATA CLEANING & EXPLICIT FEATURE ENGINEERING ---
# Real-world tabular string data must be converted to numbers before pipeline routing

# A. Clean Target Variable ('price')
if df['price'].dtype == 'object':
    df['price'] = df['price'].astype(str).str.replace('$', '', regex=False)
    df['price'] = df['price'].str.replace(',', '', regex=False)
    df['price'] = pd.to_numeric(df['price'], errors='coerce')

# B. Clean Predictor Variable ('milage')
if df['milage'].dtype == 'object':
    df['milage'] = df['milage'].astype(str).str.replace(' mi.', '', regex=False)
    df['milage'] = df['milage'].str.replace(',', '', regex=False)
    df['milage'] = pd.to_numeric(df['milage'], errors='coerce')

# Drop rows where target price or mileage is missing or corrupted
df = df.dropna(subset=['price', 'milage'])

# C. Feature Engineering: Car Age
if 'model_year' in df.columns:
    df['car_age'] = 2026 - df['model_year']

# D. Feature Engineering: Text Mining the 'engine' string
# We extract Horsepower (HP) and Engine Liters (L) directly out of the text block
if 'engine' in df.columns:
    df['engine'] = df['engine'].astype(str)
    df['horsepower'] = df['engine'].str.extract(r'(\d+\.?\d*)\s*HP').astype(float)
    df['engine_displacement_liters'] = df['engine'].str.extract(r'(\d+\.?\d*)\s*L').astype(float)

# Define X and y
# Drop original raw unparsed text/date columns that we processed
X = df.drop(columns=["price", "model_year", "engine"], errors='ignore')
y = df["price"]

# --- STEP 3: PIPELINE TRANSFORMS ---
# Organize your new columns into correct categories for the ColumnTransformer
numeric_cols = ['milage', 'car_age', 'horsepower', 'engine_displacement_liters']

# Low-cardinality text (under 15 unique values -> safe for OneHot)
low_card_cols = ['fuel_type', 'transmission', 'accident', 'clean_title']

# High-cardinality text (many unique configurations -> safe for TargetEncoding)
high_card_cols = ['brand', 'model', 'ext_col', 'int_col']

# Verify columns exist in features dataframe to prevent routing crashes
numeric_cols = [c for col in numeric_cols if (c := col) in X.columns]
low_card_cols = [c for col in low_card_cols if (c := col) in X.columns]
high_card_cols = [c for col in high_card_cols if (c := col) in X.columns]

# Build Preprocessors
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')) # Strategy handles missing regex parses cleanly
])

low_card_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

high_card_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('target', TargetEncoder(target_type="continuous")) # Encodes brands/models based on price targets
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat_low", low_card_transformer, low_card_cols),
        ("cat_high", high_card_transformer, high_card_cols)
    ]
)

# --- STEP 4: MODEL CONFIGURATION ---
# Using XGBoost here as it naturally excels at non-linear relationships found in car valuations
model_pipeline = Pipeline(steps=[
    ("preprocess", preprocess),
    ("regressor", XGBRegressor(n_estimators=300, max_depth=6, learning_rate=0.05, random_state=42))
])

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Starting training pipeline on cleaned car dataset...")
model_pipeline.fit(X_train, y_train)

# --- STEP 5: EVALUATION ---
y_pred = model_pipeline.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n--- Model Evaluation ---")
print(f"Mean Absolute Error (MAE): ${mae:,.2f}")
print(f"R-squared (R2 Score): {r2:.4f}")

# Save Pipeline Archetype
joblib.dump(model_pipeline, "car_price_model.pkl", compress=3)
print("\nOptimized Production Model Saved Successfully!")