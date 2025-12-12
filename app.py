import streamlit as st
import pandas as pd
import os

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

# ------------------------------
# Custom CSS
# ------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #c3ecff 0%, #f6e6ff 100%);
    font-family: 'Poppins', sans-serif;
}
.big-title {
    font-size: 42px;
    text-align: center;
    font-weight: 700;
    background: -webkit-linear-gradient(#7928ca, #ff0080);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.card {
    background: rgba(255, 255, 255, 0.55);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    backdrop-filter: blur(12px);
}
.stButton>button {
    background: linear-gradient(135deg, #ff416c, #ff4b2b);
    color: white;
    padding: 12px 25px;
    border-radius: 10px;
    border: none;
    font-size: 18px;
    width: 100%;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Title
# ------------------------------
st.markdown("<h1 class='big-title'>🚗 Car Price Prediction System</h1>", unsafe_allow_html=True)
st.write("### Enter the car details below and get an instant price prediction!")

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
        brand = st.selectbox("🔹 Brand", brands)
        model_name = st.selectbox("🔹 Model", brand_models[brand])
        year = st.number_input("🔹 Year", min_value=1990, max_value=2025, value=2015)

    with col2:
        engine_size = st.number_input("🔹 Engine Size (Liters)", min_value=1.0, max_value=6.0, value=2.0)
        fuel_type = st.selectbox("🔹 Fuel Type", fuel_types)
        transmission = st.selectbox("🔹 Transmission", transmissions)

    mileage = st.number_input("🔹 Mileage (KM)", min_value=0, max_value=300000, value=50000)
    condition = st.selectbox("🔹 Condition", conditions)
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------
# Dummy Predict Function
# ------------------------------
def dummy_predict(year, mileage, engine_size):
    # Simple formula: newer cars + bigger engine + less mileage = higher price
    base_price = 500000  # starting price
    price = base_price + (year - 2000) * 15000 + engine_size * 50000 - mileage * 2
    return max(price, 10000)  # minimum price 10k

# ------------------------------
# Predict Button
# ------------------------------
predict = st.button("🔮 Predict Price Now")
if predict:
    price = dummy_predict(year, mileage, engine_size)
    st.success(f"💰 **Estimated Price: ₹ {price:,.2f}**")

# ------------------------------
# Footer
# ------------------------------
st.write("---")
st.markdown("🔧 **Built with Streamlit | Dummy Prediction Mode**")
