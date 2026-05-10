import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout, BatchNormalization
from io import StringIO
import streamlit as st

class GRUModel:

    def __init__(self, optimizer, seq_len, n_features):
        self.optimizer = optimizer
        self.seq_len = seq_len
        self.n_features = n_features
        self.model = self.build_model()

    def build_model(self):
        def log_cosh_loss(y_true, y_pred):
            error = y_pred - y_true
            return tf.reduce_mean(tf.math.log(tf.math.cosh(error)))
        
        model = Sequential([
            GRU( 128, return_sequences=True, input_shape=(self.seq_len, self.n_features)),
            BatchNormalization(),
            Dropout(0.3),
            GRU(64, return_sequences=True),
            BatchNormalization(),
            Dropout(0.2),
            GRU(32, return_sequences=False),
            Dropout(0.2),
            Dense(32, activation="relu"),
            Dense(1)
        ])
        model.compile( optimizer=self.optimizer, loss=log_cosh_loss, metrics=["mae"] )
        
        stream = StringIO()
        model.summary(print_fn=lambda x: stream.write(x + "\n"))
        summary_string = stream.getvalue()
        with st.expander("View Model Summary"):
            st.code(summary_string)

        return model

    def get_model(self):
        return self.model