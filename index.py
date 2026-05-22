import streamlit as st
from styles import load_styles
import os
import hashlib
import pandas as pd

CSV_FILE = "users.csv"

def initialize_admin():
    admin_username = "admin"
    admin_email = "admin@stocksense.com"
    admin_password = "123456"
    encrypted_password = hashlib.sha256(admin_password.encode()).hexdigest()
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Full Name", "Email","Username","Password","Role"])
        admin_row = {
            "Full Name": "Administrator",
            "Email": admin_email,
            "Username": admin_username,
            "Password": encrypted_password,
            "Role": "Admin"
        }
        df = pd.concat([df, pd.DataFrame([admin_row])], ignore_index=True)
        df.to_csv(CSV_FILE,index=False)
    else:
        df = pd.read_csv(CSV_FILE)
        required_columns = ["Full Name","Email","Username","Password","Role"]
        for col in required_columns:
            if col not in df.columns:
                if col == "Role":
                    df[col] = "User"
                else:
                    df[col] = ""
        admin_exists = df[(df["Username"].astype(str).str.lower() == admin_username.lower()) & (df["Role"].astype(str).str.lower() == "admin")]
        if admin_exists.empty:
            admin_row = {
                "Full Name": "Administrator",
                "Email": admin_email,
                "Username": admin_username,
                "Password": encrypted_password,
                "Role": "Admin"
            }
            df = pd.concat([df, pd.DataFrame([admin_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

st.set_page_config(page_title="StockSense", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

initialize_admin()
load_styles()

st.markdown("""
<div class="marquee-container">
    <div class="marquee">
        Welcome to Stock Market Prediction Platform •
        Smarter Investment Planning •
        Better Financial Decisions •
        Secure User Experience •
        Market Analysis & Insights 
    </div>
</div>
""", unsafe_allow_html=True)
st.write("")

st.markdown("""
<div class='title'> StockSense </div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; font-size:22px; color:#dddddd;'> Explore market trends for Indian companies listed under NSE. Analyze their daily, weekly, monthly and yearly performances corroborated by machine learning algorithms. </p>
""", unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
        <h2>📊 Market Analysis</h2>
        <p> Explore market trends with easy visualization </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card">
        <h2>📈 Prediction System</h2>
        <p> Forecast market movement with prediction tools </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="card">
        <h2>⚡ Real-Time Analytics </h2>
        <p> Live stock performance tracking </p>
    </div>
    """, unsafe_allow_html=True)
st.write("")
st.write("")

col1, spacer, col2 = st.columns([1, 0.08, 1])
with col1:
    if st.button("🔐 Sign In", use_container_width=True):
        st.switch_page("pages/login.py")
with col2:
    if st.button("✨ Create Account", use_container_width=True):
        st.switch_page("pages/register.py")

st.markdown("""
<hr>
<div class='footer'> Stock Market Analysis </div>
""", unsafe_allow_html=True)