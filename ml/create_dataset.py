import pandas as pd
import numpy as np

data = []

for i in range(2000):

    price_change = np.random.normal(0, 0.03)
    volume = np.random.normal(100, 40)
    volatility = np.random.normal(0.02, 0.01)

    # randomly force some pump cases
    if np.random.rand() < 0.2:
        price_change = np.random.uniform(0.05, 0.15)
        volume = np.random.uniform(150, 300)
        pump = 1
    else:
        pump = 0

    data.append([price_change, volume, volatility, pump])

df = pd.DataFrame(
    data,
    columns=["price_change", "volume", "volatility", "pump"]
)

print(df["pump"].value_counts())

df.to_csv("ml/training_data.csv", index=False)