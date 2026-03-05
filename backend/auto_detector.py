import time
from ml.feature_engine import compute_features
from backend.predict import predict_pump

SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "solusdt",
    "dogeusdt",
    "bnbusdt"
]

def run_detector():

    while True:

        for symbol in SYMBOLS:

            features = compute_features(symbol)

            if features is None:
                continue

            probability = predict_pump(
                features["price_change"],
                features["volume"],
                features["volatility"]
            )

            print(symbol, "pump probability:", probability)

            if probability > 0.8:
                print(f"🚨 PUMP ALERT {symbol}")

        time.sleep(10)


if __name__ == "__main__":
    run_detector()