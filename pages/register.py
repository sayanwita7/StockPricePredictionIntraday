import streamlit as st
import pandas as pd
import os
import re
import hashlib
from styles import load_register_styles

st.set_page_config(page_title="Register", page_icon="✍️", layout="centered", initial_sidebar_state="collapsed")

CSV_FILE = "users.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Full Name", "Email", "Username", "Password", "Role"]).to_csv(CSV_FILE, index=False)

load_register_styles()

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
<div class="logo">
✍️
</div>
<div class="title">
Create Your Account
</div>
<div class="subtitle">
Join StockSense and access intelligent market insights
</div>
""", unsafe_allow_html=True)

with st.form("register_form"):
    full_name = st.text_input("👤 Full Name",placeholder="Enter your full name")
    email = st.text_input("📧 Email Address",placeholder="Enter your email")
    username = st.text_input("🧑 Username (Minimum 4 Characters)",placeholder="Choose a username")
    password = st.text_input("🔒 Password (Minimum 8 Characters - 1 Uppercase, 1 Lowercase, 1 Special Character)", type="password",placeholder="Create a strong password")
    confirm_password = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
    if confirm_password:
        if password == "":
            st.warning("⚠ Please enter password first")
        elif confirm_password == password:
            st.success("✅ Password matched")
        else:
            st.error("❌ Password does not match")
    submitted = st.form_submit_button( "✨ Create Account" )
st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    full_name = full_name.strip()
    email = email.strip()
    username = username.strip()
    if not all([full_name, email, username, password, confirm_password]):
        st.warning("⚠ Please fill all required fields")
    elif len(full_name) < 3:
        st.error("❌ Full name must contain at least 3 characters")
    elif not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",email):
        st.error("❌ Please enter a valid email address")
    elif len(username) < 4:
        st.error("❌ Username must be at least 4 characters long")
    elif " " in username:
        st.error("❌ Username cannot contain spaces")
    elif len(password) < 8:
        st.error("❌ Password must be at least 8 characters long")
    elif not re.search(r"[A-Z]", password):
        st.error("❌ Password must contain at least one uppercase letter")
    elif not re.search(r"[a-z]", password):
        st.error("❌ Password must contain at least one lowercase letter")
    elif not re.search(r"[0-9]", password):
        st.error("❌ Password must contain at least one number")
    elif not re.search(r"[!@#$%^&*]", password):
        st.error("❌ Password must contain at least one special character (!@#$%^&*)")
    elif password != confirm_password:
        st.error("❌ Passwords do not match")
    else:
        df = pd.read_csv(CSV_FILE)
        email_exists = (df["Email"].astype(str).str.lower().eq(email.lower()).any())
        username_exists = (df["Username"].astype(str).str.lower().eq(username.lower()).any())
        if email_exists:
            st.error("❌ Email already registered")
        elif username_exists:
            st.error("❌ Username already exists")
        else:
            encrypted_password = hashlib.sha256(password.encode()).hexdigest()
            new_user = pd.DataFrame([{
                "Full Name": full_name,
                "Email": email,
                "Username": username,
                "Password": encrypted_password,
                "Role": "User"
            }])
            df = pd.concat([df, new_user],ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            st.success("✅ Registration successful! Redirecting to login...")
            st.switch_page("pages/login.py")

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
            "<p class='bottom-text'>Already have an account?</p>",
            unsafe_allow_html=True)
   
with col2:
    st.page_link("pages/login.py", label="Sign In")
