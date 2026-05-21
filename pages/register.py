import streamlit as st
import pandas as pd
import os
from styles import load_register_styles

st.set_page_config(page_title="Register", page_icon="✍️", layout="centered", initial_sidebar_state="collapsed")

CSV_FILE = "users.csv"
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Full Name", "Email", "Username", "Password"]).to_csv(CSV_FILE, index=False)

load_register_styles()
if st.button("⬅ Return to Main Page"):
    st.switch_page("index.py")

st.markdown("""
<div class="card">
<div class="logo">
✍️
</div>
<div class="title">
Create Account
</div>
<div class="subtitle">
Create your stock dashboard account
</div>
""", unsafe_allow_html=True)

with st.form("register_form"):
    full_name = st.text_input("👤 Full Name")
    email = st.text_input("📧 Email Address")
    username = st.text_input("🧑 Username")
    password = st.text_input("🔒 Password", type="password")
    confirm_password = st.text_input("🔐 Confirm Password", type="password")
    submitted = st.form_submit_button( "Create Account" )

st.markdown("</div>", unsafe_allow_html=True)
if submitted:
    if (not full_name or not email or not username or not password or not confirm_password ):
        st.warning("Please fill all fields")
    elif password != confirm_password:
        st.error( "Passwords do not match!")
    else:
        df = pd.read_csv(CSV_FILE)
        email_exists = (df["Email"].astype(str).str.lower().eq(email.lower()).any())
        username_exists = (df["Username"].astype(str).str.lower().eq(username.lower()).any())
        if email_exists:
            st.error("Email already registered!")
        elif username_exists:
            st.error("Username already exists!")
        else:
            new_user = pd.DataFrame([{
                "Full Name": full_name,
                "Email": email,
                "Username": username,
                "Password": password
            }])
            df = pd.concat([df, new_user],ignore_index=True)
            df.to_csv(CSV_FILE,index=False)
            st.success("Registration Successful!")
            st.switch_page("pages/login.py")

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
            "<p class='bottom-text'>Already have an account?</p>",
            unsafe_allow_html=True)
    
with col2:
    st.page_link("pages/login.py", label="Sign In")
    
    