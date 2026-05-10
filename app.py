import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from datainput.data import StockData
from pipelines.prediction_pipeline import EvaluateGRU
from visualisation.testpredictionplot import TestPredictionPlot
from visualisation.candlestickplot import CandlestickPlot

st.title("Intraday Stock Price Prediction Using GRU")
st.markdown("This project aims to develop a deep learning-based stock price prediction system for Indian companies using freely accessible intraday stock market data.")

st.subheader("Data Input: ")
st.markdown( "The stock market data used in this dashboard has been fetched using yfinance. Interactive intraday candlestick charts for all loaded trading days are available below for detailed visualization and analysis.")
stock = StockData( ticker_name="RELIANCE.NS", period="8d", interval="1m")
df = stock.get_dataframe()

#Plotting loaded data
day_groups = df.groupby(df.index.date)
for date, group in day_groups:
    with st.expander(f"View Data for {date}"):
        chart = CandlestickPlot(
            df=group,
            date=date
        )
        chart.show_chart()

df_test, df_train, df_val = stock.get_test_train_val_dataframe(df)
X_train, y_train, X_val, y_val, X_test, y_test_scaled = stock.get_X_Y_data(df_test, df_train, df_val)

st.subheader("Dataset Sizes: ")
st.markdown("Test, train and validation data was divided as follows: \nThe data from the latest date was reserved for testing, the data from the day before was reserved for validation and the rest for training.")
st.write("Train Data Length:", len(X_train))
st.write("Validation Data Length:", len(X_val))
st.write("Test Data Length:", len(X_test))

st.subheader("Training: ")
st.markdown ("The GRU model has been trained using 100 epochs and a batch-size of 32 (model processes 32 training samples at a time before updating its weights). However, two callbacks are implemented to improve training: EarlyStopping to terminate training when further learning is no longer beneficial and ReduceLROnPlateau to dynamically reduce the learning rate when the model’s performance stops improving.")
#Model Training and Prediction
close_scaler = MinMaxScaler()
evaluator = EvaluateGRU(
    ticker_name="RELIANCE.NS",
    period="8d",
    interval="1m",
    seq_len=50,
    n_features=5
)
y_test, y_pred, mae, rmse, mape = evaluator.run()


st.subheader("Results: ")
st.markdown("Here are the results from the predictions using GRU: ")
results_df = pd.DataFrame({
    "Actual Price (₹)": y_test,
    "Predicted Price (₹)": y_pred,
    "Error (₹)": y_test - y_pred
}).round(2)
st.dataframe(results_df)

col1, col2, col3 = st.columns(3)
col1.metric("MAE", f"₹{mae:.2f}")
col2.metric("RMSE", f"₹{rmse:.2f}")
col3.metric("MAPE", f"{mape:.2f}%")

#Plotting Predictions on test data
plotter = TestPredictionPlot(
    df_test=df_test,
    y_test=y_test,
    y_pred=y_pred,
    seq_len=50
)
fig = plotter.create_plot()
st.plotly_chart(fig, use_container_width=True)

