import numpy as np
import plotly.graph_objects as go

class TestPredictionPlot:
    def __init__(self, df_test, y_test, y_pred, seq_len=50, n_ticks=20):
        self.df_test = df_test
        self.y_test = y_test
        self.y_pred = y_pred
        self.seq_len = seq_len
        self.n_ticks = n_ticks

    def create_plot(self):
        test_dates = self.df_test.index[self.seq_len:]
        x = np.arange(len(self.y_test))
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=x,
                y=self.y_test,
                mode="lines",
                name="Actual Close"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=x,
                y=self.y_pred,
                mode="lines",
                name="Predicted Close",
                line=dict(dash="dash")
            )
        )
        tick_positions = np.linspace( 0,len(x) - 1, self.n_ticks, dtype=int)
        tick_labels = [ test_dates[i].strftime("%H:%M") for i in tick_positions]
        fig.update_layout(
            title="GRU — Intraday Close Price Prediction",
            xaxis=dict(title="Time Steps", tickmode="array", tickvals=tick_positions, ticktext=tick_labels),
            yaxis=dict(title="Price (₹)"),
            template="plotly_white",
            hovermode="x unified",
            height=500,
            width=1200
        )
        return fig

    def show_plot(self):
        fig = self.create_plot()
        fig.show()