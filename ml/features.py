import pandas as pd

def generate_features(df):

    df["price_change"] = df["price"].pct_change()

    df["volume"] = df["quantity"].rolling(10).sum()

    df["volatility"] = df["price"].rolling(10).std()

    return df