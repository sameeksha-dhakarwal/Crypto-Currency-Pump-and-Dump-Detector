from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("sqlite:///crypto.db")

def store_trade(symbol, price, quantity, timestamp):

    df = pd.DataFrame({
        "symbol": [symbol],
        "price": [price],
        "quantity": [quantity],
        "timestamp": [timestamp]
    })

    df.to_sql("trades", engine, if_exists="append", index=False)