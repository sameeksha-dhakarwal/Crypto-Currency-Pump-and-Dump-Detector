import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("ml/training_data.csv")

X = df[["price_change","volume","volatility"]]
y = df["pump"]

model = RandomForestClassifier()

model.fit(X,y)

joblib.dump(model,"ml/pump_model.pkl")

print("Model trained")