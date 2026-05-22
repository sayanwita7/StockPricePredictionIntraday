import streamlit as st
import pandas as pd
import os
import hashlib
from styles import load_login_styles

st.set_page_config(page_title="Login", page_icon="🔑", layout="centered", initial_sidebar_state="collapsed")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

CSV_FILE = "users.csv"

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Full Name", "Email", "Username", "Password", "Role"]).to_csv(CSV_FILE, index=False)

load_login_styles()

st.markdown("""
    <style>
    /* Hide default Streamlit multipage navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("⬅ Return to Main Page"):
    st.switch_page("index.py")

st.markdown("""
<div class="card">
<div class="logo"> 🔑 </div>
<div class="title"> Welcome Back </div>
<div class="subtitle"> Sign in to access your StockSense dashboard </div>
""", unsafe_allow_html=True)

with st.form("login_form"):
    role = st.selectbox("🧑 Role",["User", "Admin"])
    username = st.text_input("👤 Username", placeholder="Enter your username")
    password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
    submitted = st.form_submit_button("🔐 Sign In")

st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    username = username.strip()
    password = password.strip()
    if username == "" and password == "":
        st.error("⚠ Please enter username and password")
    elif username == "":
        st.warning("⚠ Username is required")
    elif password == "":
        st.warning("⚠ Password is required")
    else:
        df = pd.read_csv(CSV_FILE)
        user_exists = df[df["Username"].astype(str).str.lower() == username.lower()]
        if user_exists.empty:
            st.error("❌ Username not found")
        else:
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()
            if role == "Admin":
                admin_user = df[(df["Username"].astype(str).str.lower()== username.lower())&(df["Password"].astype(str)== encrypted_password)&(df["Role"].astype(str).str.lower()== "admin")]
                if admin_user.empty:
                    role_check = user_exists[user_exists["Role"].astype(str).str.lower() == "admin"]
                    if role_check.empty:
                        st.error("❌ This account is not registered as Admin")
                    else:
                        st.error("❌ Incorrect password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.username = (admin_user.iloc[0]["Username"])
                    st.session_state.email = (admin_user.iloc[0]["Email"])
                    st.session_state.full_name = (admin_user.iloc[0]["Full Name"])
                    st.success(f"👑 Welcome Admin, {username}")
                    st.switch_page("pages/adminDashboard.py")
            else:
                user = df[(df["Username"].astype(str).str.lower()== username.lower())&(df["Password"].astype(str)== encrypted_password)&(df["Role"].astype(str).str.lower()== "user")]
                if user.empty:
                    role_check = user_exists[user_exists["Role"].astype(str).str.lower()== "user"]
                    if role_check.empty:
                        st.error("❌ This account is not registered as User")
                    else:
                        st.error("❌ Incorrect password")
                else:
                    st.session_state.logged_in = True
                    st.session_state.role = "user"
                    st.session_state.username = (user.iloc[0]["Username"])
                    st.session_state.email = (user.iloc[0]["Email"])
                    st.session_state.full_name = (user.iloc[0]["Full Name"])
                    st.success(f"✅ Welcome back, {username}")
                    st.switch_page("pages/userDashboard.py")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<p class='bottom-text'>Don't have an account?</p>", unsafe_allow_html=True)
with col2:
    st.page_link("pages/register.py", label="Register")
