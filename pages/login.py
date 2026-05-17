import streamlit as st
import pandas as pd
import os
from styles import load_login_styles

st.set_page_config(page_title="Login", page_icon="📈", layout="centered", initial_sidebar_state="collapsed")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

CSV_FILE = "users.csv"

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Full Name", "Email", "Username", "Password"]).to_csv(CSV_FILE, index=False)


load_login_styles()

if st.button("⬅ Return to Main Page"):
    st.switch_page("index.py")

st.markdown("""
<div class="card">
<div class="logo"> 📈 </div>
<div class="title"> Login </div>
<div class="subtitle"> Log In to Your Dashboard </div>
""", unsafe_allow_html=True)

with st.form("login_form"):
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    submitted = st.form_submit_button("Login")

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not username or not password:
        st.warning("Please enter username and password!")
    else:
        df = pd.read_csv(CSV_FILE)
        user = df[(df["Username"].astype(str).str.lower()== username.lower())&(df["Password"].astype(str)== password)]
        if not user.empty:
            st.session_state.logged_in = True
            st.session_state.username = (user.iloc[0]["Username"])
            st.session_state.email = (user.iloc[0]["Email"])
            st.session_state.full_name = (user.iloc[0]["Full Name"])
            st.success(f"Welcome {username}")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Invalid username or password")

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("<p class='bottom-text'>Don't have an account?</p>", unsafe_allow_html=True)
with col2:
    st.page_link("pages/register.py", label="Register")