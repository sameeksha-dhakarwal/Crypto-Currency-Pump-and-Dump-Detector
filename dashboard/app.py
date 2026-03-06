import sys
import os
import time

# Allow Streamlit to access project modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

from ml.feature_engine import compute_features
from backend.predict import predict_pump


# Database connection
engine = create_engine("sqlite:///crypto.db")

# Coins to monitor
SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "solusdt",
    "dogeusdt",
    "bnbusdt"
]

# Page configuration
st.set_page_config(page_title="Crypto Pump Detector", layout="wide")

st.title("🚨 AI Crypto Pump Monitoring System")
st.markdown("Real-time pump-and-dump surveillance dashboard")

st.divider()


# ===============================
# Pump Probability Gauges
# ===============================

st.header("Pump Probability Gauges")

gauge_cols = st.columns(len(SYMBOLS))

for i, symbol in enumerate(SYMBOLS):

    with gauge_cols[i]:

        features = compute_features(symbol)

        if features:

            prob = predict_pump(
                features["price_change"],
                features["volume"],
                features["volatility"]
            )

            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prob,
                title={"text": symbol.upper()},
                gauge={
                    "axis": {"range": [0, 1]},
                    "bar": {"color": "red"},
                    "steps": [
                        {"range": [0, 0.5], "color": "green"},
                        {"range": [0.5, 0.8], "color": "orange"},
                        {"range": [0.8, 1], "color": "red"}
                    ]
                }
            ))

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write("Collecting data...")


# ===============================
# Crypto Market Board
# ===============================

st.divider()
st.header("Crypto Market Board")

board_cols = st.columns(len(SYMBOLS))

for i, symbol in enumerate(SYMBOLS):

    with board_cols[i]:

        query = f"""
        SELECT * FROM trades
        WHERE symbol='{symbol}'
        ORDER BY timestamp DESC
        LIMIT 50
        """

        df = pd.read_sql(query, engine)

        if len(df) > 0:

            latest_price = df.iloc[0]["price"]
            first_price = df.iloc[-1]["price"]

            change = (latest_price - first_price) / first_price

            color = "green" if change > 0 else "red"

            st.markdown(
                f"""
                <div style="padding:20px;background:{color};color:white;border-radius:10px;text-align:center">
                <h3>{symbol.upper()}</h3>
                <h2>${latest_price:.2f}</h2>
                <p>{change*100:.2f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.write("Waiting for data")


# ===============================
# Live Price Charts
# ===============================

st.divider()
st.header("Live Price Charts")

chart_cols = st.columns(len(SYMBOLS))

for i, symbol in enumerate(SYMBOLS):

    with chart_cols[i]:

        query = f"""
        SELECT * FROM trades
        WHERE symbol='{symbol}'
        ORDER BY timestamp DESC
        LIMIT 200
        """

        df = pd.read_sql(query, engine)

        if len(df) > 0:

            df = df.sort_values("timestamp")

            fig = px.line(
                df,
                x="timestamp",
                y="price",
                title=symbol.upper()
            )

            st.plotly_chart(fig, use_container_width=True)


# ===============================
# Volume Heatmap
# ===============================

st.divider()
st.header("Volume Spike Heatmap")

query = """
SELECT symbol, quantity FROM trades
ORDER BY timestamp DESC
LIMIT 500
"""

df = pd.read_sql(query, engine)

pivot = df.groupby("symbol").sum()

fig, ax = plt.subplots()

sns.heatmap(
    pivot,
    annot=True,
    cmap="Reds",
    ax=ax
)

st.pyplot(fig)


# ===============================
# Recent Trades
# ===============================

st.divider()
st.header("Recent Trades")

df = pd.read_sql(
    "SELECT * FROM trades ORDER BY timestamp DESC LIMIT 100",
    engine
)

st.dataframe(df, use_container_width=True)


# ===============================
# Auto Refresh
# ===============================

time.sleep(5)
st.rerun()