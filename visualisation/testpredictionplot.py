import numpy as np
import plotly.graph_objects as go

class TestPredictionPlot:
    def __init__(self, df_test, y_test, y_pred):
        self.df_test = df_test
        self.y_test = y_test
        self.y_pred = y_pred
        self.seq_len = 50
        self.n_ticks = 20

    def create_plot(self):
        test_dates = self.df_test.index[self.seq_len:]
        x = test_dates
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=test_dates,
                y=self.y_test,
                mode="lines",
                name="Actual Close"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=test_dates,
                y=self.y_pred,
                mode="lines",
                name="Predicted Close"
            )
        )
        fig.update_layout(
            title="Intraday Close Price Prediction",
            xaxis_title="Time",
            yaxis_title="Price (₹)",
            template="plotly_white",
            hovermode="x unified"
        )
        fig.update_xaxes(
            tickformat="%H:%M",
            tickangle=270,
            showgrid=True,
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True
        )

        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            showline=True,
            linewidth=2,
            linecolor="black",
            mirror=True
        )
        fig.update_xaxes(
            dtick=15*60 * 1000,   
            tickformat="%H:%M"
        )
        return fig
