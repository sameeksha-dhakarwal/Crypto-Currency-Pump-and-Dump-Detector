import sys
import os
import time

# allow Streamlit to import project modules
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


# ===============================
# DATABASE
# ===============================

engine = create_engine("sqlite:///crypto.db")

SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "solusdt",
    "dogeusdt",
    "bnbusdt"
]


# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Crypto Pump Detector",
    layout="wide"
)

st.title(" AI Crypto Pump Monitoring System")
st.write("Real-time monitoring for pump-and-dump activity")

st.divider()


# ===============================
# PUMP PROBABILITY GAUGES
# ===============================

st.header(" Pump Probability")

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
            st.info("Collecting data...")


# ===============================
# CRYPTO MARKET BOARD
# ===============================

st.divider()
st.header(" Crypto Market Board")

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

        if len(df) > 1:

            latest_price = df.iloc[0]["price"]
            old_price = df.iloc[-1]["price"]

            change = (latest_price - old_price) / old_price

            if change >= 0:
                color = "#66d494"
            else:
                color = "#c24c4c"

            st.markdown(
                f"""
                <div style="
                background:{color};
                padding:20px;
                border-radius:10px;
                text-align:center;
                color:white;">
                <h3>{symbol.upper()}</h3>
                <h2>${latest_price:.2f}</h2>
                <h4>{change*100:.2f}%</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.write("Waiting for data...")


# ===============================
# LIVE PRICE CHARTS
# ===============================

st.divider()
st.header(" Live Price Charts")

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

            # convert timestamp for readability
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

            fig = px.line(
                df,
                x="timestamp",
                y="price",
                title=symbol.upper(),
                markers=False
            )

            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=30, b=10)
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.write("Waiting for chart data...")


# ===============================
# VOLUME HEATMAP
# ===============================

st.divider()
st.header(" Volume Spike Heatmap")

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
# RECENT TRADES
# ===============================

st.divider()
st.header(" Recent Trades")

df = pd.read_sql(
    "SELECT * FROM trades ORDER BY timestamp DESC LIMIT 100",
    engine
)

st.dataframe(df, use_container_width=True)


# ===============================
# AUTO REFRESH
# ===============================

time.sleep(5)
st.rerun()