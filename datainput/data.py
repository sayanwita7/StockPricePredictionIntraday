import yfinance as yf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class StockData:
    def __init__(self, ticker_name, period, interval):
        self.ticker_name = ticker_name
        self.period = period
        self.interval = interval

    def get_company_info(self):
        ticker = yf.Ticker(self.ticker_name)
        hist = ticker.history(period="2d")
        info = ticker.info
        prev = hist["Close"].iloc[-2]
        last = hist["Close"].iloc[-1]
        change = ((last - prev) / prev) * 100
        arrow = "▲" if change >= 0 else "▼"
        revenue = info.get("totalRevenue")
        debt = info.get("totalDebt")
        debt_ratio = (debt/revenue if debt and revenue else None)
        data = {
            "Company": info.get("shortName", self.ticker_name.replace(".NS", "")),
            "Sector": info.get("sector", "-"),
            "Close (₹)": round(last, 2),
            "Change %": f"{arrow} {change:.2f}%",
            "P/E": info.get("trailingPE", "-"),
            "52W High (₹)": info.get("fiftyTwoWeekHigh","-"),
            "52W Low (₹)": info.get("fiftyTwoWeekLow", "-"),
            "Debt/Revenue": f"{debt_ratio:.2f}"  if debt_ratio is not None else "-"
        }
        return data

    def get_dataframe(self):
        ticker = yf.Ticker(self.ticker_name)
        df = ticker.history( period=self.period, interval=self.interval)
        df.drop('Dividends', axis=1, inplace=True)
        df.drop('Stock Splits', axis=1, inplace=True)
        return df
    
    def get_test_train_val_dataframe(self, df):
        df['Date'] = df.index.date
        df['Time'] = df.index.time
        latest_two = df['Date'].sort_values().unique()[-2:]
        split_date_train_val = latest_two[0]
        split_date_test_train = latest_two[1]
        df_before = df[df['Date'] < split_date_test_train]
        df_test = df[df['Date'] >= split_date_test_train]        
        df_train = df_before[df_before['Date'] < split_date_train_val]
        df_val  = df_before[df_before['Date'] >= split_date_train_val]
        
        df_test = df_test[["Open", "High", "Low", "Close", "Volume"]].copy()
        df_train = df_train[["Open", "High", "Low", "Close", "Volume"]].copy()
        df_val = df_val[["Open", "High", "Low", "Close", "Volume"]].copy()

        return df_test, df_train, df_val
        
    def get_X_Y_data(self, df_test, df_train, df_val):
        scaler = MinMaxScaler()
        close_scaler = MinMaxScaler()

        df_train.dropna(inplace=True)
        train_scaled = scaler.fit_transform(df_train)
        close_scaler.fit_transform(df_train[["Close"]])

        df_val.dropna(inplace=True)
        val_scaled = scaler.fit_transform(df_val)
        close_scaler.fit_transform(df_val[["Close"]])

        df_test.dropna(inplace=True)
        test_scaled = scaler.fit_transform(df_test)
        close_scaler.fit_transform(df_test[["Close"]])

        def create_sequences(data, seq_len=50):
            X, y = [], []
            for i in range(len(data) - seq_len):
                X.append(data[i : i + seq_len])
                y.append(data[i + seq_len][3])
            return np.array(X), np.array(y)

        SEQ_LEN = 50
        X_train, y_train = create_sequences(train_scaled, SEQ_LEN)
        X_val, y_val = create_sequences(val_scaled, SEQ_LEN)
        X_test, y_test_scaled = create_sequences(test_scaled, SEQ_LEN)

        y_train_actual = close_scaler.inverse_transform(y_train.reshape(-1, 1))
        y_val_actual = close_scaler.inverse_transform(y_val.reshape(-1, 1))
        y_test_actual = close_scaler.inverse_transform(y_test_scaled.reshape(-1, 1))

        return X_train, y_train, y_train_actual, X_val, y_val, y_val_actual, X_test, y_test_scaled, y_test_actual, close_scaler



