import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///crypto.db")

def load_trades(symbol):

    query = f"""
    SELECT * FROM trades
    WHERE symbol = '{symbol}'
    ORDER BY timestamp DESC
    LIMIT 200
    """

    df = pd.read_sql(query, engine)

    df = df.sort_values("timestamp")

    return df


def compute_features(symbol):

    df = load_trades(symbol)

    if len(df) < 20:
        return None

    price_change = (df["price"].iloc[-1] - df["price"].iloc[0]) / df["price"].iloc[0]

    volume = df["quantity"].sum()

    volatility = df["price"].std()

    return {
        "price_change": price_change,
        "volume": volume,
        "volatility": volatility
    }