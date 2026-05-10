import plotly.graph_objects as go
import streamlit as st


class CandlestickPlot:
    def __init__(self, df, date):
        self.df = df.copy()
        self.date = date

    def prepare_data(self):
        self.df['Hour'] = self.df.index.hour
        self.df['Time'] = ( self.df.index.strftime('%H:%M'))

    def create_chart(self):
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=self.df['Time'],
                open=self.df['Open'],
                high=self.df['High'],
                low=self.df['Low'],
                close=self.df['Close'],
                increasing_line_color='#00C853',
                decreasing_line_color='#D50000',
                increasing_fillcolor='#00C853',
                decreasing_fillcolor='#D50000',
                name='Price'
            )
        )

        fig.update_layout(
            title=f"Intraday Candlestick ({self.date})",
            xaxis_title="Time",
            yaxis_title="Price (₹)",
            height=600,
            xaxis_rangeslider_visible=True,
            hovermode="x unified",
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )
        )

        fig.update_xaxes( showgrid=False, tickangle=-90)
        fig.update_yaxes( showgrid=True, gridcolor='rgba(255,255,255,0.08)')
        return fig

    def show_chart(self):
        self.prepare_data()
        fig = self.create_chart()
        st.title(self.date)
        st.plotly_chart(fig, use_container_width=True)