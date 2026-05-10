import numpy as np
from tensorflow.keras.callbacks import ( EarlyStopping, ReduceLROnPlateau)
from sklearn.preprocessing import MinMaxScaler
from datainput.data import StockData
from model.GRUModel import GRUModel
from visualisation.streamlitcallback import StreamlitCallback

class TrainGRU:

    def __init__( self, ticker_name, period, interval, seq_len, n_features,  optimizer="adam"):
        self.ticker_name = ticker_name
        self.period=period
        self.interval=interval
        self.seq_len = seq_len
        self.n_features = n_features
        self.optimizer = optimizer
        self.model = None
        self.history = None
        # self.close_scaler= None

    def prepare_data(self):
        stock = StockData(ticker_name=self.ticker_name, period=self.period, interval=self.interval)
        df = stock.get_dataframe()
        df_test, df_train, df_val = (stock.get_test_train_val_dataframe(df))
        (self.X_train, self.y_train, self.X_val, self.y_val, self.X_test, self.y_test_scaled) = stock.get_X_Y_data(df_test, df_train, df_val )
        self.close_scaler = MinMaxScaler()
        self.close_scaler.fit(df_train[['Close']])

    def build_model(self):
        gru = GRUModel( optimizer=self.optimizer, seq_len=self.seq_len, n_features=self.n_features)
        self.model = gru.get_model()

    def train(self):

        callbacks = [
            StreamlitCallback(),
            EarlyStopping(
                monitor="val_loss",
                patience=10,
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.5,
                patience=5,
                min_lr=1e-6
            )
        ]
        self.history = self.model.fit(
            self.X_train,
            self.y_train,
            validation_data=(
                self.X_val,
                self.y_val
            ),
            epochs=100,
            batch_size=32,
            callbacks=callbacks
        )

    def run(self):
        self.prepare_data()
        self.build_model()
        self.train()
        return self.model, self.history