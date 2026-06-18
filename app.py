import streamlit as st
import pandas as pd
import numpy as np
import joblib
import re

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# ------------------------------
# Custom CSS (Real Car Photo Background & Glassmorphism)
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Poppins', sans-serif;
}

/* ---------- REALISTIC BACKGROUND IMAGE ---------- */
[data-testid="stAppViewContainer"] {
    background-image: url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Ensure main block background is transparent to show the Unsplash image */
[data-testid="stHeader"], [data-testid="stContentBlock"] {
    background: transparent !important;
}

.big-title {
    font-size: 42px;
    text-align: center;
    font-weight: 800;
    color: #ffffff;
    padding-top: 10px;
    padding-bottom: 5px;
    text-shadow: 0px 4px 20px rgba(0,0,0,0.6);
}

.sub-title {
    text-align: center;
    color: #f0f0f0;
    margin-bottom: 30px;
    text-shadow: 0px 2px 10px rgba(0,0,0,0.5);
}

/* ---------- GLASSMORPHISM CARD ---------- */
div[data-testid="stVerticalBlock"] > div:has(div.card-marker) {
    background: rgba(255, 255, 255, 0.15) !important;
    padding: 30px !important;
    border-radius: 25px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

/* Label text color tuning for dark backgrounds */
label {
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background: linear-gradient(135deg, #111111, #333333) !important;
    color: white !important;
    padding: 12px 25px !important;
    border-radius: 50px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    font-size: 18px !important;
    width: 100% !important;
    cursor: pointer !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #000000, #222222) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6) !important;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 14px;
    color: white;
    opacity: 0.8;
    text-shadow: 0px 2px 6px rgba(0,0,0,0.6);
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Model Loading Pipeline
# ------------------------------
@st.cache_resource
def load_production_model():
    # Safely load the compiled scikit-learn pipeline archetype
    return joblib.load("car_price_model.pkl")

try:
    model_pipeline = load_production_model()
except Exception as e:
    st.error(f"⚠️ Model Loading Failed. The actual error is: {e}")
    st.stop()

# ------------------------------
# App Headers
# ------------------------------
st.markdown("<div class='big-title'>Car Price Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Enter the exact vehicle configuration below to determine valuation.</div>", unsafe_allow_html=True)

# ------------------------------
# Core Layout Form
# ------------------------------
# This empty markdown acts as a handle for our custom CSS to style this specific container card
st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)

with st.container():
    # Reference values sourced directly from categories within your real-world dataset
    brand_list = ['Ford', 'Hyundai', 'Lexus', 'INFINITI', 'Audi', 'Acura', 'BMW', 'Tesla', 
                  'Land', 'Aston', 'Toyota', 'Lincoln', 'Jaguar', 'Mercedes-Benz', 'Nissan', 'Porsche']
    
    fuel_options = ['Gasoline', 'Diesel', 'Electric', 'Hybrid', 'Plug-In Hybrid', 'E85 Flex Fuel']
    transmission_options = ['Automatic', 'Manual', '6-Speed A/T', '8-Speed Automatic', '7-Speed A/T', '6-Speed M/T', 'CVT']
    accident_options = ['None reported', 'At least 1 accident or damage reported']

    col1, col2 = st.columns(2)
    
    with col1:
        selected_brand = st.selectbox("Brand Name", brand_list)
        selected_model = st.text_input("Specific Model / Trim", value="911 Carrera S")
        selected_year = st.slider("Model Year", min_value=1995, max_value=2026, value=2019)
        mileage_val = st.number_input("Current Mileage (Pure Integer)", min_value=0, max_value=400000, value=25000)

    with col2:
        selected_fuel = st.selectbox("Engine Fuel Baseline", fuel_options)
        engine_desc = st.text_input("Engine String Block (e.g., 420.0HP 3.0L V6)", value="420.0HP 3.0L Flat 6 Cylinder")
        selected_trans = st.selectbox("Gearbox Architecture", transmission_options)
        clean_title = st.selectbox("Ownership Title Status", ["Yes", "No"])

    st.markdown("---")
    col3, col4 = st.columns(2)
    
    with col3:
        selected_accident = st.selectbox("Historical Incidents", accident_options)
        ext_color = st.text_input("Exterior Finish Paint", value="Black")
        
    with col4:
        int_color = st.text_input("Interior Cabin Material Trim", value="Black")

# ------------------------------
# Inference Execution Pipeline
# ------------------------------
if st.button("Calculate Market Valuation"):
    
    # 1. Structure raw web inputs to mirror a DataFrame row matching training columns
    raw_payload = {
        "brand": [selected_brand],
        "model": [selected_model],
        "model_year": [selected_year],
        "milage": [float(mileage_val)], # Kept naming aligned with dataset column spelling
        "fuel_type": [selected_fuel],
        "engine": [engine_desc],
        "transmission": [selected_trans],
        "ext_col": [ext_color],
        "int_col": [int_color],
        "accident": [selected_accident],
        "clean_title": [clean_title]
    }
    
    df_inference = pd.DataFrame(raw_payload)
    
    try:
        # 2. Re-apply data parsing logic to calculate advanced engineering columns
        df_inference['car_age'] = 2026 - df_inference['model_year']
        
        # Regex text miners extract float metrics natively from the description box string
        df_inference['horsepower'] = df_inference['engine'].str.extract(r'(\d+\.?\d*)\s*HP').astype(float).fillna(250.0)
        df_inference['engine_displacement_liters'] = df_inference['engine'].str.extract(r'(\d+\.?\d*)\s*L').astype(float).fillna(2.5)
        
        # Drop raw fields that were discarded prior to feeding the transformer layers
        processed_features = df_inference.drop(columns=["model_year", "engine"], errors='ignore')
        
        # 3. Request predictions from preprocessor + regressor ensemble pipeline
        valuation_output = model_pipeline.predict(processed_features)[0]
        
        # 4. Display result cleanly back to user (Dataset base values are priced in USD)
        st.markdown("### Evaluation Matrix Complete")
        st.success(f"💰 **Estimated Fair Market Value: ${valuation_output:,.2f} USD**")
        
    except Exception as transformation_error:
        st.error(f"Execution Aborted: Transformation parsing conflict occurred. Details: {transformation_error}")

# ------------------------------
# Footer
# ------------------------------
st.markdown("<div class='footer'>Production Pipeline Engine • Status: Operational</div>", unsafe_allow_html=True)