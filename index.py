import streamlit as st
from styles import load_styles

st.set_page_config(page_title="Stock Market Website", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
load_styles()

st.markdown("""
<div class='title'> Stock Market Prediction </div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'> Smart Investing • Better Market Insights • Future Planning </div>
""", unsafe_allow_html=True)

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
<h2 style='text-align:center; color:white;'> Welcome to Smart Investing </h2>
<p style='text-align:center; font-size:22px; color:#dddddd;'> Explore market trends, analyze performance and make smarter investment decisions with this stock prediction platform. </p>
""", unsafe_allow_html=True)
st.write("")
st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="card">
        <h2>📊 Market Analysis</h2>
        <p> Explore market trends and performance with easy visualization. </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="card">
        <h2>📈 Prediction System</h2>
        <p> Forecast market movement with advanced prediction tools. </p>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="card">
        <h2>🔒 Secure Platform</h2>
        <p> Fast, reliable and secure experience for all users. </p>
    </div>
    """, unsafe_allow_html=True)
st.write("")
st.write("")

col1, spacer, col2 = st.columns([1, 0.08, 1])
with col1:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/login.py")
with col2:
    if st.button("📝 Register", use_container_width=True):
        st.switch_page("pages/register.py")

st.markdown("""
<hr>
<div class='footer'> Stock Market Prediction </div>
""", unsafe_allow_html=True)