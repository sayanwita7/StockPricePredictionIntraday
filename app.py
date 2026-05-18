import streamlit as st
from datainput.data import StockData
from visualisation.testpredictionplot import TestPredictionPlot
from visualisation.candlestickplot import CandlestickPlot
from pipelines.prediction import Prediciton

st.title("Intraday Stock Price Prediction")
st.markdown("This project aims to develop a machine learning-based stock price prediction system for Indian companies using freely accessible intraday stock market data.")

st.subheader("Data Input: ")
st.markdown( "The stock market data used in this dashboard has been fetched using yfinance. Interactive intraday candlestick charts for all loaded trading days are available below for detailed visualization and analysis.")
stock = StockData( ticker_name="TCS.NS", period="8d", interval="1m")
with st.spinner("Fetching Stock Prices... Please wait"):
    df = stock.get_dataframe()
df_test, df_train, df_val= stock.get_test_train_val_dataframe(df)

day_groups = df.groupby(df.index.date)
for date, group in day_groups:
    with st.expander(f"View Data for {date}"):
        chart = CandlestickPlot(
            df=group,
            title=f"Intraday Data for {date}",
            x=group.index
        )
        chart.show_chart()

prediction = Prediciton(ticker_name="TCS.NS", period="8d", interval="1m")
with st.spinner("Training models... Please wait"):
    best_model_df, summary_df = prediction.run()

st.subheader("Model Performance:")
st.dataframe(summary_df)

st.subheader("Predictions:")
plotter = TestPredictionPlot(df_test, best_model_df["Actual"], best_model_df["Predicted"])
fig = plotter.create_plot()
st.plotly_chart(fig, width='content')



