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
import yfinance as yf

from datainput.data import StockData
from pipelines.prediction import Prediciton
from visualisation.testpredictionplot import TestPredictionPlot
from visualisation.candlestickplot import CandlestickPlot
from styles import load_dashboard_styles, load_settings_styles

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

st.set_page_config( page_title="StockSense", page_icon="📈", layout="wide")

load_dashboard_styles()

with st.sidebar:

    selected = option_menu(
        menu_title="StockSense",
        options=["Home","Historical Data","Stock Analysis","Settings","Logout"],
        icons=["house","clock-history","graph-up-arrow","gear","power"],
        default_index=0,
        styles={
             "container":{
                "background-color":"#121212",
                "padding":"10px",
                "border-radius":"10px"
            },
            "icon":{"color":"white"},
            "nav-link":{
                "font-size":"16px",
                "text-align":"left",
                "--hover-color":"rgba(59,130,246,0.18)"
            },
            "nav-link-selected": {
                "background": "#27129F",
                "color": "white",
            },
        }
    )

@st.cache_data
def load_tickers():
    df = pd.read_csv("tickers.csv")
    return df["ticker"].dropna().tolist()

def color_change(val):
    if "▲" in str(val):
        return "#22c55e"
    elif "▼" in str(val):
        return "#ef4444"
    return "gray"

if selected == "Home":
    st.markdown("<h1 style='text-align:center;'>🏢 Market Overview</h1>", unsafe_allow_html=True)
    st.write("A stock represents partial ownership in a company, offering a claim on its earnings and assets. As the company's value rises or falls, so does the value of its stock. Stocks are generally bought and sold electronically through stock exchanges. The main stock exchanges in India are the National Stock Exchange of India Limited (NSE) and the Bombay Stock Exchange (BSE), both located in Mumbai.")
    with st.spinner("Fetching data... Please wait"):
        tickers = load_tickers()
        table_tickers = random.sample(tickers, 30)
        card_tickers = random.sample(tickers, 3)
        cards = []
        table_data = []

        for ticker in table_tickers:
            stock = StockData(ticker_name=ticker, period="2d", interval="1d")
            data = stock.get_company_info()
            price = data["Close (₹)"]
            change = data["Change %"]
            color = color_change(change)
            table_data.append(data)

        for ticker in card_tickers:
            try:
                stock = StockData(ticker_name=ticker, period="2d", interval="1d")
                data = stock.get_company_info()
                price = data["Close (₹)"]
                change = data["Change %"]
                color = color_change(change)
                cards.append((ticker, price, change, color))
            except Exception:
                cards.append((ticker, None, None, "gray"))

    cols = st.columns(3)
    for i, (ticker, price, change, color) in enumerate(cards):
        with cols[i]:
            if price is None:
                st.markdown(f"""
                <div class="card">
                    <div class="label">
                        {ticker.replace('.NS','')}
                    </div>
                    <div class="metric">
                        Loading...
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <div class="label">
                        {ticker.replace('.NS','')}
                    </div>
                    <div class="metric">
                        ₹{price:.2f}
                    </div>
                    <div style="color:{color}; font-weight:bold;">
                        {change}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    df_table = pd.DataFrame(table_data)
    st.markdown("Information about the company's sector, today's close price, change from previous day's close price, 52-week High and Low price has been listed below. Besides these, P/E ratio and Debt/Revenue ratio has also been listed. P/E or Price-to-Earnings ratio of a company is the ratio of the company's share price to the company's earnings per share. This ratio is used for valuing companies and to find out whether they are overvalued or undervalued. Debt-to-revenue ratio measures total liabilities against total revenue, indicating how leveraged a business is. A lower ratio implies the company generates substantially more income than its debt, giving it financial freedom.")
    st.markdown("Here is the detailed information about select Indian Companies listed under NSE: ")
    styled_df = df_table.style.map(lambda x: f"color:{color_change(x)}", subset=["Change %"]).format({
        "Close (₹)": "{:.2f}",
        "P/E": "{:.2f}",
        "52W High (₹)": "{:.2f}",
        "52W Low (₹)": "{:.2f}"
    })
    st.table(styled_df)

elif selected == "Historical Data":
    st.markdown("<h1 style='text-align:center;'>📈 Historical Market View</h1>", unsafe_allow_html=True)
    
    tickers = load_tickers()
    selected_company = st.selectbox("Select Company: ", tickers)
    tab1, tab2, tab3, tab4 = st.tabs([ "Last Day", "Last Week", "Last Month", "Last Year" ])

    with tab1:
        st.subheader("Previous Day Market View")
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
            CandlestickPlot( df=yday_df, title="Intraday Overview", x=yday_df['Time']).show_chart()

    with tab2:
        st.subheader("Weekly Market View")
        df = StockData( ticker_name=selected_company, period="8d", interval="1m" ).get_dataframe().copy()
        df = df.sort_index()
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        df["date"] = df.index.date
        df = df[(df["date"] != today)]
        CandlestickPlot( df=df, title="Weekly Intraday Overview", x=df.index).show_chart()
        
        st.markdown("---")
        st.subheader("Select Day from this Week: ")
        df["date"] = df.index.date
        selected_day = st.selectbox( "Choose Day", sorted(df["date"].unique()), key="week_day_select")
        day_df = df[df["date"] == selected_day]
        CandlestickPlot( df=day_df, title=f"Intraday Overview - {selected_day}", x=day_df.index).show_chart()
        
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
            st.subheader("Select Day from this Month: ")
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
                CandlestickPlot( df=day_df, title=f"Intraday Overview - {selected_date}", x=day_df.index).show_chart()
                
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
        CandlestickPlot( df=df, title=f"Yearly Overview", x=df.index).show_chart()

elif selected == "Stock Analysis":
    st.markdown("<h1 style='text-align:center;'> 💹 Analysis for Today</h1>", unsafe_allow_html=True)
    st.subheader("Today's Market View")
    def load_tickers():
        df = pd.read_csv("tickers.csv")
        return df["ticker"].dropna().tolist()
    tickers = load_tickers()
    selected_company = st.selectbox("Select Company: ", tickers)
    stock = StockData( ticker_name=selected_company, period="1d", interval="1m")
    df= stock.get_dataframe()
    date = df.index.date[-1]
    CandlestickPlot( df=df, title=f"Today's Overview: {date}", x=df.index).show_chart()

    st.subheader("Here's the model prediction for today: ")
    stock = StockData( ticker_name=selected_company, period="8d", interval="1m")
    df= stock.get_dataframe()
    df_test, df_train, df_val= stock.get_test_train_val_dataframe(df)
    prediction = Prediciton(ticker_name=selected_company, period="8d", interval="1m")
    with st.spinner("Training models... Please wait"):
        best_model_df, summary_df = prediction.run()
    plotter = TestPredictionPlot(df_test, best_model_df["Actual"], best_model_df["Predicted"])
    fig = plotter.create_plot()
    st.plotly_chart(fig,  use_container_width=True)

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