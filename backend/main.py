from fastapi import FastAPI
from backend.predict import predict_pump

app = FastAPI()

@app.get("/")
def home():

    return {"message":"Crypto Pump Detector Running"}

@app.post("/detect")

def detect(price_change:float,volume:float,volatility:float):

    probability = predict_pump(price_change,volume,volatility)

    return {"pump_probability":probability}