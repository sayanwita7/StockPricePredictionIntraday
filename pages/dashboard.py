import contextlib
import io
import logging
import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import random
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

from datainput.data import StockData
from pipelines.prediction import Prediciton
from visualisation.testpredictionplot import TestPredictionPlot
from visualisation.candlestickplot import CandlestickPlot
from styles import load_sidebar_styles, load_dashboard_styles, load_settings_styles

logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("keras").setLevel(logging.ERROR)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

@contextlib.contextmanager
def hide_stdout():
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

if "df_test" not in st.session_state:
    st.session_state.df_test = None

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

load_dashboard_styles()

with st.sidebar:
    load_sidebar_styles()
    selected = option_menu(
        menu_title="Stock AI",
        options=["Home","Historical Data","Stock Analysis","Settings","Logout"],
        icons=["house","clock-history","graph-up-arrow","gear","power"],
        default_index=0,
        styles={
            "container":{"background-color":"transparent"},
            "icon":{"color":"white"},
            "nav-link":{
                "font-size":"16px",
                "text-align":"left",
                "--hover-color":"rgba(59,130,246,0.18)"
            },
            "nav-link-selected": {
                "background": "#C47BE4",
                "color": "white",
            },
        }
    )

st.markdown(
    '<p class="title">📈 Stock Market Dashboard</p>',
    unsafe_allow_html=True
)

stock = StockData( ticker_name="RELIANCE.NS", period="8d", interval="1m")
with st.spinner("Fetching Stock Prices... Please wait"):
    df = stock.get_dataframe()
df_test, df_train, df_val= stock.get_test_train_val_dataframe(df)

@st.cache_data
def load_tickers():
    df = pd.read_csv("tickers.csv")
    return df["ticker"].dropna().tolist()

# Home Tab
if selected == "Home":
    st.subheader("📊 Market Overview")
    st.markdown("Here are the close prices for twelve Indian companies: ")
    with st.spinner("Fetching data... Please wait"):
        tickers = load_tickers()
        selected_tickers = random.sample(tickers, 12)
        cols = st.columns(3)
        cards = []
        for ticker in selected_tickers:
            try:
                stock = StockData( ticker_name=ticker, period="2d", interval="1d")
                df= stock.get_dataframe()
                prev = df["Close"].iloc[-2]     
                last = df["Close"].iloc[-1]     
                change = ((last - prev) / last) * 100
                arrow = "▲" if change >= 0 else "▼"
                color = "#22c55e" if change >= 0 else "#ef4444"
                cards.append((ticker, last, change, arrow, color))
            except:
                cards.append((ticker, None, None, None, "gray"))
    
    for i, (ticker, price, change, arrow, color) in enumerate(cards):
        col = cols[i%3]
        with col:
            if price is None:
                st.markdown(f"""
                <div class="card">
                    <div class="label">{ticker.replace('.NS','')}</div>
                    <div class="metric">Loading...</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <div class="label">{ticker.replace('.NS','')}</div>
                    <div class="metric">₹{price:.2f}</div>
                    <div style="color:{color}; font-weight:bold;">
                        {arrow} {change:.2f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)

#Historical Data Tab
elif selected == "Historical Data":
    st.markdown("<h1 style='text-align:center;'>📈 Historical Market Data Dashboard</h1>", unsafe_allow_html=True)
    
    tickers = load_tickers()
    selected_company = st.selectbox("Select Company", tickers)
    tab1, tab2, tab3, tab4 = st.tabs([ "📅 1 Day", "📊 1 Week", "📆 1 Month", "📈 1 Year" ])

    with tab1:
        st.subheader("Previous Day Candlestick")
        stock = StockData( ticker_name=selected_company, period="2d", interval="1m")
        df= stock.get_dataframe()
        df["date"] = df.index.date
        all_days = sorted(df["date"].unique())
        if len(all_days) < 2:
            st.warning("Not enough data to compute yesterday view")
        else:
            yesterday = all_days[-2]
            yday_df = df[df["date"] == yesterday].drop(columns=["date"])
            st.write(f"Showing data for: {yesterday}")
            yday_df['Time'] = ( yday_df.index.strftime('%H:%M'))
            CandlestickPlot( df=yday_df, title="Intraday Candlestick", x=yday_df['Time']).show_chart()

    with tab2:
        st.subheader("Weekly Market View")
        df = StockData( ticker_name=selected_company, period="8d", interval="1m" ).get_dataframe().copy()
        df = df.sort_index()
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        df["date"] = df.index.date
        df = df[(df["date"] != today)]
        CandlestickPlot( df=df, title="Weekly Intraday Candlestick", x=df.index).show_chart()
        
        st.markdown("---")
        st.subheader("🔎 Select Day for Focus View")
        df["date"] = df.index.date
        selected_day = st.selectbox( "Choose Day", sorted(df["date"].unique()), key="week_day_select")
        day_df = df[df["date"] == selected_day]
        CandlestickPlot( df=day_df, title=f"Intraday Candlestick - {selected_day}", x=day_df.index).show_chart()
        
    with tab3:
            st.subheader("Monthly Market View")
            stock = StockData( ticker_name=selected_company, period="1mo", interval="5m")
            df = stock.get_dataframe()
            if df is None or df.empty:
                st.warning("No data available")
                st.stop()
            df = df.copy()
            df = df.sort_index()
            today = datetime.today().date()
            df["date"] = df.index.date
            df = df[df["date"] < today]
            CandlestickPlot( df=df, title=f"Monthly Overview", x=df.index).show_chart()
            
            st.markdown("---")
            st.subheader("Select Day")
            unique_dates = sorted(df["date"].unique())
            selected_date = st.date_input( "Pick Date", value=unique_dates[-1], min_value=unique_dates[0], max_value=unique_dates[-1])
            intraday_df = StockData( ticker_name=selected_company, period="1mo", interval="5m").get_dataframe()
            if intraday_df is None or intraday_df.empty:
                st.warning("No intraday data available")
                st.stop()
            intraday_df = intraday_df.copy()
            intraday_df["date"] = intraday_df.index.date
            day_df = intraday_df[intraday_df["date"] == selected_date]
            if day_df.empty:
                st.warning("No intraday data for selected date")
            else:
                CandlestickPlot( df=day_df, title=f"Intraday View - {selected_date}", x=day_df.index).show_chart()
                
    with tab4:
        st.subheader("Yearly Market View")
        df = StockData( ticker_name=selected_company, period="1y", interval="1h").get_dataframe().copy()
        if df is None or df.empty:
            st.warning("No data available")
            st.stop()
        df = df.sort_index()
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        df["date"] = df.index.date
        df = df[ (df["date"] != today) & (df["date"] != yesterday)]
        cutoff_date = today - timedelta(days=365)
        df = df[df["date"] >= cutoff_date]
        CandlestickPlot( df=df, title=f"Yearly Candlestick", x=df.index).show_chart()

#Stock Analysis
elif selected == "Stock Analysis":
    #Plotting today's candlestick
    st.subheader("Today's Market View")
    def load_tickers():
        df = pd.read_csv("tickers.csv")
        return df["ticker"].dropna().tolist()
    tickers = load_tickers()
    selected_company = st.selectbox("Select Company", tickers)
    stock = StockData( ticker_name=selected_company, period="1d", interval="1m")
    df= stock.get_dataframe()
    date = df.index.date[-1]
    CandlestickPlot( df=df, title=f"Today's Candlestick: {date}", x=df.index).show_chart()

    # ADD TABLE!

    #Plotting Predictions
    st.subheader("Model Prediction: ")
    prediction = Prediciton(ticker_name=selected_company, period="8d", interval="1m")
    with st.spinner("Training models... Please wait"):
        best_model_df, summary_df = prediction.run()
    plotter = TestPredictionPlot(df_test, best_model_df["Actual"], best_model_df["Predicted"])
    fig = plotter.create_plot()
    st.plotly_chart(fig, width='content')
    
# SETTINGS
elif selected == "Settings":

    st.title("⚙️ Settings")
    st.write("Manage your stock dashboard preferences.")
    load_settings_styles()
    st.markdown("""
    
    """, unsafe_allow_html=True)
    st.subheader("👤 Account Settings")
    full_name = st.text_input( "Full Name", value=st.session_state.full_name)
    username = st.text_input("Change Username",value=st.session_state.username)
    email = st.text_input( "Email Address", value=st.session_state.email)
    if st.button("Save Account Settings"):
        st.session_state.full_name = full_name
        st.session_state.username = username
        st.session_state.email = email
        st.success("Account Settings Updated")

    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="setting-card">
    """, unsafe_allow_html=True)

    st.subheader("🔒 Security Settings")
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password",type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Update Password"):
        if new_password != confirm_password:
            st.error( "Passwords do not match")
        elif new_password == "":
            st.warning( "Enter new password")
        else:
            st.success("Password Updated Successfully")
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)

elif selected == "Logout":
    st.session_state.logged_in = False
    st.success("Logged Out Successfully")
    st.switch_page("index.py")