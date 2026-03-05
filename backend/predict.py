import joblib
import os

# absolute path to model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml/pump_model.pkl")

model = joblib.load(MODEL_PATH)


def predict_pump(price_change, volume, volatility):

    features = [[price_change, volume, volatility]]

    probability = model.predict_proba(features)[0][1]

    return float(probability)