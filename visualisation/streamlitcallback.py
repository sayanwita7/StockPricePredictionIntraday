import streamlit as st
from tensorflow.keras.callbacks import Callback


class StreamlitCallback(Callback):

    def on_train_begin(self, logs=None):
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()

    def on_epoch_end(self, epoch, logs=None):
        progress = (epoch + 1) / self.params['epochs']
        self.progress_bar.progress(progress)
        self.status_text.text(
            f"Epoch {epoch+1}/{self.params['epochs']} "
            f"- loss: {logs['loss']:.4f} "
            f"- val_loss: {logs['val_loss']:.4f}"
        )