import streamlit as st
import pandas as pd
import random
import plotly.express as px
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta

from styles import load_settings_styles
from datainput.data import StockData
from pipelines.prediction import Prediciton
from visualisation.candlestickplot import CandlestickPlot
from visualisation.testpredictionplot import TestPredictionPlot

if "logged_in" not in st.session_state or st.session_state.role != "admin":
    st.error("🚫 Unauthorized Access")
    st.stop()

st.set_page_config(page_title="StockSense Admin", layout="wide")

st.markdown("""
    <style>
    /* Hide default Streamlit multipage navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

def plot_metric(df, metric):
    plot_df = df[["Model", f"Train {metric}", f"Validation {metric}", f"Test {metric}"]]
    plot_df = plot_df.melt(id_vars="Model", var_name="Dataset", value_name="Value")
    plot_df["Dataset"] = plot_df["Dataset"].str.replace(f" {metric}", "", regex=False)
    fig = px.bar( plot_df, x="Dataset", y="Value", color="Model", barmode="group", text="Value", title=f"{metric} Comparison Across Models")
    fig.update_traces( texttemplate='%{text:.4f}', textposition='outside')
    fig.update_layout( xaxis_title="Dataset", yaxis_title=metric, height=600)
    st.plotly_chart(fig, use_container_width=True, key=f"{metric}_chart")

def load_tickers():
    df = pd.read_csv("tickers.csv")
    return df["ticker"].dropna().tolist()

def color_change(val):
    if "▲" in str(val):
        return "#22c55e"
    elif "▼" in str(val):
        return "#ef4444"
    return "gray"

with st.sidebar:
    page = option_menu(
        menu_title="StockSense",
        options=["Home","Stock Data","Models", "Settings", "Logout"],
        icons=["house","database-fill", "robot", "gear-fill","power"],
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

if page == "Home":
    st.markdown("<h1 style='text-align:center;'>Market Overview</h1>", unsafe_allow_html=True)
    st.markdown("The available data being accessed using yFinance is available to view under the Stock Data tab. The model training results and other parameters is available under Models tab. Here's a quick market overview: ")
    
    with st.spinner("Fetching data... Please wait"):
        tickers = load_tickers()
        table_tickers = random.sample(tickers, 30)
        table_data = []

        for ticker in table_tickers:
            stock = StockData(ticker_name=ticker, period="2d", interval="1d")
            data = stock.get_company_info()
            price = data["Close (₹)"]
            change = data["Change %"]
            color = color_change(change)
            table_data.append(data)

    df_table = pd.DataFrame(table_data)
    styled_df = df_table.style.map(lambda x: f"color:{color_change(x)}", subset=["Change %"]).format({
        "Close (₹)": "{:.2f}",
        "P/E": "{:.2f}",
        "52W High (₹)": "{:.2f}",
        "52W Low (₹)": "{:.2f}"
    })
    st.table(styled_df)
   
elif page == "Stock Data":
    st.markdown("<h1 style='text-align:center;'> Available Market View</h1>", unsafe_allow_html=True)
    tickers = load_tickers()
    selected_company = st.selectbox("Select Company: ", tickers)
    tab1, tab2, tab3 = st.tabs([ "Last Day", "Last Week", "Last Month" ])

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
                
elif page == "Models":
    st.markdown("<h1 style='text-align:center;'>Model Training & Evaluation</h1>", unsafe_allow_html=True)
    tickers = load_tickers()
    ticker = st.selectbox("Select Company: ", tickers)

    stock = StockData( ticker_name=ticker, period="8d", interval="1m")
    df= stock.get_dataframe()
    df_test, df_train, df_val= stock.get_test_train_val_dataframe(df)
    
    st.markdown("Test, train and validation data was divided as follows: \nThe data from the latest date was reserved for testing, the data from the day before was reserved for validation and the rest for training.")
    st.write("Train Data Length:", len(df_train))
    st.write("Validation Data Length:", len(df_val))
    st.write("Test Data Length:", len(df_test))

    prediction = Prediciton( ticker_name=ticker, period="8d", interval="1m" )
    with st.spinner("Training models..."):
        best_model_df, summary_df = prediction.run()
        df_plot, best_model_name = prediction.get_prediction_dataframe()           
    st.session_state.summary_df = summary_df
    st.session_state.best_model_df = best_model_df
    st.success("✅ Training Completed")

    for col in df_plot.columns:
        if col != "Actual":
            st.subheader(f"Actual Vs {col} Prediction:")
            plotter = TestPredictionPlot(df_test, df_plot["Actual"], df_plot[col])
            fig = plotter.create_plot()
            st.plotly_chart(fig,  use_container_width=True,  key=f"prediction_{col}")

    st.subheader("Model Performance")
    st.dataframe(summary_df)

    plot_metric(summary_df, "RMSE")
    plot_metric(summary_df, "MSE")
    plot_metric(summary_df, "MAPE")

    st.subheader(f"Hence, Best Model picked here is: {best_model_name}")
    plotter = TestPredictionPlot(df_test, best_model_df["Actual"], best_model_df["Predicted"])
    fig = plotter.create_plot()
    st.plotly_chart(fig,  use_container_width=True, key=f"best_model_{best_model_name}")

elif page == "Settings":
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

elif page == "Logout":
    st.session_state.clear()
    st.switch_page("index.py")
