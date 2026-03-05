import sys
import os

# add project root to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from ml.feature_engine import compute_features
from backend.predict import predict_pump

engine = create_engine("sqlite:///crypto.db")

SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "solusdt",
    "dogeusdt",
    "bnbusdt"
]

st.set_page_config(page_title="Crypto Pump Detector", layout="wide")

st.title("🚨 Crypto Pump-and-Dump Detector")

cols = st.columns(len(SYMBOLS))

for i, symbol in enumerate(SYMBOLS):

    with cols[i]:

        st.subheader(symbol.upper())

        features = compute_features(symbol)

        if features:

            probability = predict_pump(
                features["price_change"],
                features["volume"],
                features["volatility"]
            )

            st.metric(
                label="Pump Probability",
                value=f"{probability:.2f}"
            )

            if probability > 0.8:
                st.error("🚨 Pump Alert!")

        else:
            st.write("Waiting for data...")

# show latest trades
st.header("Recent Trades")

df = pd.read_sql(
    "SELECT * FROM trades ORDER BY timestamp DESC LIMIT 50",
    engine
)

st.dataframe(df)