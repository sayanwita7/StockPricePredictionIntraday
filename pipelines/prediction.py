import numpy as np
from tensorflow.keras.callbacks import ( EarlyStopping, ReduceLROnPlateau)
from sklearn.metrics import mean_squared_error, root_mean_squared_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
from datainput.data import StockData
from model.Models import Models
import lightgbm as lgb
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

class Prediciton:

    def __init__( self, ticker_name, period, interval):
        self.ticker_name = ticker_name
        self.period=period
        self.interval=interval
        self.all_results=[]
        self.model = None

    def prepare_data(self):
        stock = StockData(ticker_name=self.ticker_name, period=self.period, interval=self.interval)
        df = stock.get_dataframe()
        df_test, df_train, df_val = (stock.get_test_train_val_dataframe(df))
        self.X_train, self.y_train, self.y_train_actual, self.X_val, self.y_val, self.y_val_actual, self.X_test, self.y_test_scaled, self.y_test_actual, self.scaler = stock.get_X_Y_data(df_test, df_train, df_val )

    def evaluate_model(self, model_name, y_train, y_val, y_test, y_pred_train, y_pred_val, y_pred_test):
        scaler=self.scaler
        y_pred_train_actual = scaler.inverse_transform(y_pred_train.reshape(-1, 1))
        y_pred_val_actual = scaler.inverse_transform(y_pred_val.reshape(-1, 1))
        y_pred_test_actual = scaler.inverse_transform(y_pred_test.reshape(-1, 1))
        y_train_actual = scaler.inverse_transform(y_train.reshape(-1, 1))
        y_val_actual = scaler.inverse_transform(y_val.reshape(-1, 1))
        y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))
        results = {
            "Model": model_name,
            "y_pred_train_actual": y_pred_train_actual,
            "y_pred_val actual": y_pred_val_actual,
            "y_pred_test_actual": y_pred_test_actual,
            "Train MSE": mean_squared_error(y_train_actual, y_pred_train_actual),
            "Validation MSE": mean_squared_error(y_val_actual, y_pred_val_actual),
            "Test MSE": mean_squared_error(y_test_actual, y_pred_test_actual),
            "Train RMSE": root_mean_squared_error(y_train_actual, y_pred_train_actual),
            "Validation RMSE": root_mean_squared_error(y_val_actual, y_pred_val_actual),
            "Test RMSE": root_mean_squared_error(y_test_actual, y_pred_test_actual),
            "Train MAPE": mean_absolute_percentage_error(y_train_actual,y_pred_train_actual),
            "Validation MAPE": mean_absolute_percentage_error(y_val_actual, y_pred_val_actual),
            "Test MAPE": mean_absolute_percentage_error(y_test_actual, y_pred_test_actual)
        }
        return results

    def train(self):
        model_builder=Models()
        self.ridge_model = model_builder.get_ridge_model()
        self.svm_model = model_builder.get_svm_model()
        self.rf_model = model_builder.get_random_forest_model()

        self.X_train_flat = self.X_train.reshape(self.X_train.shape[0], -1)
        self.X_val_flat   = self.X_val.reshape(self.X_val.shape[0], -1)
        self.X_test_flat  = self.X_test.reshape(self.X_test.shape[0], -1)

        self.svm_model.fit(self.X_train_flat, self.y_train)
        self.rf_model.fit(self.X_train_flat, self.y_train)
        self.ridge_model.fit(self.X_train_flat, self.y_train)

        best_k = None
        best_rmse = float('inf')
        for k in range(1, 31):
            model = model_builder.get_knn_model(k)
            model.fit(self.X_train_flat, self.y_train)
            pred = model.predict(self.X_val_flat)
            rmse = np.sqrt(mean_squared_error(self.y_val, pred))
            if rmse < best_rmse:
                best_rmse = rmse
                best_k = k
        self.knn_model = model_builder.get_knn_model(best_k)
        self.knn_model.fit(self.X_train_flat, self.y_train)

        self.lgbm_model = model_builder.get_lgbm_model()
        callbacks = [lgb.early_stopping(stopping_rounds=100, verbose=False), lgb.log_evaluation(period=0)]
        self.lgbm_model.fit( self.X_train_flat, self.y_train, eval_set=[(self.X_train_flat, self.y_train), (self.X_val_flat, self.y_val)], eval_metric="l2", callbacks=callbacks)

        # self.gru_model = model_builder.get_gru_model(n_features = self.X_train.shape[2])
        # callbacks = [EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True), ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6)]
        # self.gru_model.fit( self.X_train, self.y_train, validation_data = (self.X_val, self.y_val), epochs = 40 , batch_size = 32, callbacks  = callbacks)

    def predict(self):
        y_pred_train = self.svm_model.predict(self.X_train_flat)
        y_pred_val = self.svm_model.predict(self.X_val_flat)
        y_pred_test = self.svm_model.predict(self.X_test_flat)
        svm_results = self.evaluate_model(
            model_name="SVM",
            y_train=self.y_train,
            y_val=self.y_val,
            y_test=self.y_test_scaled,
            y_pred_train=y_pred_train,
            y_pred_val=y_pred_val,
            y_pred_test=y_pred_test,
        )

        self.all_results.append(svm_results)

        y_pred_train = self.rf_model.predict(self.X_train_flat)
        y_pred_val = self.rf_model.predict(self.X_val_flat)
        y_pred_test = self.rf_model.predict(self.X_test_flat)

        rf_results = self.evaluate_model(
            model_name="Random Forest",
            y_train=self.y_train,
            y_val=self.y_val,
            y_test=self.y_test_scaled,
            y_pred_train=y_pred_train,
            y_pred_val=y_pred_val,
            y_pred_test=y_pred_test,
        )

        self.all_results.append(rf_results)

        y_pred_train = self.knn_model.predict(self.X_train_flat)
        y_pred_val = self.knn_model.predict(self.X_val_flat)
        y_pred_test = self.knn_model.predict(self.X_test_flat)

        knn_results = self.evaluate_model(
            model_name="KNN",
            y_train=self.y_train,
            y_val=self.y_val,
            y_test=self.y_test_scaled,
            y_pred_train=y_pred_train,
            y_pred_val=y_pred_val,
            y_pred_test=y_pred_test,
        )
        self.all_results.append(knn_results)

        
        y_pred_train = self.lgbm_model.predict(self.X_train_flat)
        y_pred_val = self.lgbm_model.predict(self.X_val_flat)
        y_pred_test = self.lgbm_model.predict(self.X_test_flat)

        lgb_results = self.evaluate_model(
            model_name="LightGBM",
            y_train=self.y_train,
            y_val=self.y_val,
            y_test=self.y_test_scaled,
            y_pred_train=y_pred_train,
            y_pred_val=y_pred_val,
            y_pred_test=y_pred_test
        )
        self.all_results.append(lgb_results)

        y_pred_train = self.ridge_model.predict(self.X_train_flat)
        y_pred_val = self.ridge_model.predict(self.X_val_flat)
        y_pred_test = self.ridge_model.predict(self.X_test_flat)

        ridge_results = self.evaluate_model(
            model_name="Ridge",
            y_train=self.y_train,
            y_val=self.y_val,
            y_test=self.y_test_scaled,
            y_pred_train=y_pred_train,
            y_pred_val=y_pred_val,
            y_pred_test=y_pred_test,
        )
        self.all_results.append(ridge_results)

        # y_pred_train = self.gru_model.predict(self.X_train)
        # y_pred_val = self.gru_model.predict(self.X_val)
        # y_pred_test = self.gru_model.predict(self.X_test)

        # gru_results = self.evaluate_model(
        #     model_name="GRU",
        #     y_train=self.y_train,
        #     y_val=self.y_val,
        #     y_test=self.y_test_scaled,
        #     y_pred_train=y_pred_train,
        #     y_pred_val=y_pred_val,
        #     y_pred_test=y_pred_test,
        # )
        # self.all_results.append(gru_results)
    
    def evaluate(self):
        results = pd.DataFrame(self.all_results)
        self.summary_df = results[["Model", "Train RMSE", "Validation RMSE", "Test RMSE", "Train MSE", "Validation MSE", "Test MSE", "Train MAPE", "Validation MAPE", "Test MAPE"]]
        self.summary_df = self.summary_df.round(4)
        self.summary_df = self.summary_df.sort_values(by=["Validation RMSE", "Test RMSE"])
        self.summary_df = self.summary_df.reset_index(drop=True)
        results = results.sort_values(by=["Validation RMSE", "Test RMSE"])
        best_model = results.iloc[0]
        self.best_model_df = pd.DataFrame({
            "Actual": self.y_test_actual.flatten(),
            "Predicted": best_model["y_pred_test_actual"].flatten()
        })

    def run(self):
        self.prepare_data()
        self.train()
        self.predict()
        self.evaluate()
        return self.best_model_df, self.summary_df