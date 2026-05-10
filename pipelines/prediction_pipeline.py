import numpy as np
from sklearn.metrics import (mean_absolute_error, mean_squared_error)
from pipelines.training_pipeline import TrainGRU


class EvaluateGRU:
    def __init__(self, ticker_name, period, interval, seq_len, n_features):
        self.ticker_name = ticker_name
        self.period = period
        self.interval = interval
        self.seq_len = seq_len
        self.n_features = n_features
        self.model = None
        self.history = None
        self.y_pred = None
        self.y_test = None

    def train_model(self):
        trainer = TrainGRU(
            ticker_name=self.ticker_name,
            period=self.period,
            interval=self.interval,
            seq_len=self.seq_len,
            n_features=self.n_features
        )
        self.model, self.history = trainer.run()
        self.close_scaler = trainer.close_scaler
        self.X_test = trainer.X_test
        self.y_test_scaled = trainer.y_test_scaled

    def predict(self):
        y_pred_scaled = (self.model.predict(self.X_test).flatten())
        self.y_pred = (self.close_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten())
        self.y_test = (self.close_scaler.inverse_transform(self.y_test_scaled.reshape(-1, 1)).flatten())

    def evaluate(self):
        mae = mean_absolute_error(self.y_test,self.y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test,self.y_pred))
        mape = np.mean(np.abs((self.y_test - self.y_pred)/self.y_test))*100
        return self.y_test, self.y_pred, mae, rmse, mape

    def run(self):
        self.train_model()
        self.predict()
        return self.evaluate()