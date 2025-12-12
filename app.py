import streamlit as st
import pandas as pd
import os

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="",
    layout="centered"
)

# ------------------------------
# Custom CSS (Real Car Photo Background)
# ------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body {
    font-family: 'Poppins', sans-serif;
}

/* ---------- REALISTIC BACKGROUND IMAGE ---------- */
body {
    background-image: url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.big-title {
    font-size: 48px;
    text-align: center;
    font-weight: 800;
    color: #ffffff;
    padding: 20px;
    text-shadow: 0px 4px 20px rgba(0,0,0,0.6);
}

/* ---------- GLASSMORPHISM CARD ---------- */
.card {
    background: rgba(255, 255, 255, 0.25);
    padding: 30px;
    border-radius: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.35);
    transition: 0.3s ease-in-out;
}

.card:hover {
    transform: scale(1.02);
    box-shadow: 0 12px 40px rgba(0,0,0,0.7);
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background: linear-gradient(135deg, #222, #444);
    color: white;
    padding: 15px 25px;
    border-radius: 50px;
    border: none;
    font-size: 20px;
    width: 100%;
    cursor: pointer;
    font-weight: 600;
    letter-spacing: 1px;
    transition: 0.25s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.stButton>button:hover {
    transform: translateY(-4px);
    background: linear-gradient(135deg, #000, #333);
    box-shadow: 0 10px 25px rgba(0,0,0,0.7);
}

/* ---------- FOOTER ---------- */
.footer {
    text-align: center;
    margin-top: 40px;
    font-size: 15px;
    color: white;
    opacity: 0.7;
    text-shadow: 0px 2px 6px rgba(0,0,0,0.6);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------
# Title
# ------------------------------
st.markdown("<h1 class='big-title'>Car Price Prediction System</h1>", unsafe_allow_html=True)
st.write("### Enter the car details below to generate an estimated market value.")

# ------------------------------
# Car Details Input
# ------------------------------
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    brands = ['Tesla', 'BMW', 'Audi', 'Ford']
    brand_models = {
        "Tesla": ["Model X", "Model Y"],
        "BMW": ["5 Series"],
        "Audi": ["A4"],
        "Ford": ["Mustang"]
    }
    fuel_types = ['Petrol', 'Diesel', 'Electric']
    transmissions = ['Manual', 'Automatic']
    conditions = ['New', 'Used', 'Like New']

    col1, col2 = st.columns(2)
    with col1:
        brand = st.selectbox("Brand", brands)
        model_name = st.selectbox("Model", brand_models[brand])
        year = st.number_input("Year", min_value=1990, max_value=2025, value=2015)

    with col2:
        engine_size = st.number_input("Engine Size (Liters)", min_value=1.0, max_value=6.0, value=2.0)
        fuel_type = st.selectbox("Fuel Type", fuel_types)
        transmission = st.selectbox("Transmission", transmissions)

    mileage = st.number_input("Mileage (KM)", min_value=0, max_value=300000, value=50000)
    condition = st.selectbox("Condition", conditions)

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Dummy Predict Function
# ------------------------------
def dummy_predict(year, mileage, engine_size):
    base_price = 500000  
    price = base_price + (year - 2000) * 15000 + engine_size * 50000 - mileage * 2
    return max(price, 10000)

# ------------------------------
# Predict Button
# ------------------------------
predict = st.button("Predict Price")
if predict:
    price = dummy_predict(year, mileage, engine_size)
    st.success(f"Estimated Price: ₹ {price:,.2f}")

# ------------------------------
# Footer
# ------------------------------
st.markdown("<div class='footer'>One-Step before purchase</div>", unsafe_allow_html=True)
