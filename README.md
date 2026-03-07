# AI Cryptocurrency Pump-and-Dump Monitoring System

A **real-time full-stack AI system** that monitors cryptocurrency markets and detects potential **pump-and-dump activity** using machine learning.

The system streams **live trading data from Binance**, stores it in a database, extracts market features, predicts pump probability using an ML model, and visualizes everything in a **real-time dashboard**.

---

# Project Overview

Cryptocurrency markets are vulnerable to **coordinated pump-and-dump schemes**, where prices are artificially inflated before a rapid sell-off.

This project detects such behavior by combining:

* **Real-time data streaming**
* **Feature engineering**
* **Machine learning predictions**
* **Interactive data visualization**

The result is a **live monitoring platform** that continuously analyzes market activity.

---

# System Architecture

```
Binance WebSocket API
        │
        ▼
Trade Stream (Python WebSocket Client)
        │
        ▼
SQLite Database
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Pump Detection
        │
        ▼
Real-Time Dashboard (Streamlit)
```

---

# Features

## Real-Time Data Streaming

* Connects to **Binance WebSocket API**
* Streams live trades for multiple cryptocurrencies
* Stores data in a local SQLite database

Coins currently monitored:

```
BTCUSDT
ETHUSDT
SOLUSDT
DOGEUSDT
BNBUSDT
```

---

## Machine Learning Pump Detection

The system analyzes recent trading activity and calculates:

* **Price Change**
* **Trading Volume**
* **Price Volatility**

These features are fed into a **Random Forest classifier** trained to estimate **pump probability**.

Example output:

```
BTCUSDT pump probability: 0.02
SOLUSDT pump probability: 0.37
DOGEUSDT pump probability: 0.32
```

---

## Interactive Dashboard

Built with **Streamlit + Plotly**, the dashboard provides:

### Pump Probability Gauges

Displays ML prediction for each cryptocurrency.

### Crypto Market Board

Shows:

* Current price
* Percentage change
* Color-coded market tiles

### Live Price Charts

Real-time price charts for each coin.

### Volume Activity Heatmap

Detects spikes in trading activity.

### Recent Trades Table

Displays latest transactions stored in the database.

---

# Project Structure

```
Crypto-Pump-and-Dump-Detector
│
├── backend
│   ├── main.py
│   ├── auto_detector.py
│   └── predict.py
│
├── data_ingestion
│   └── binance_stream.py
│
├── database
│   └── db.py
│
├── dashboard
│   └── app.py
│
├── ml
│   ├── create_dataset.py
│   ├── feature_engine.py
│   ├── train_model.py
│   └── model.pkl
│
├── crypto.db
├── requirements.txt
└── README.md
```

---

# Installation

## 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/crypto-pump-detector.git
cd crypto-pump-detector
```

---

## 2. Create Virtual Environment

```
python -m venv venv
```

Activate environment

### Windows

```
venv\Scripts\activate
```

### Mac/Linux

```
source venv/bin/activate
```

---

## 3. Install Dependencies

```
pip install -r requirements.txt
```

Or manually install:

```
pip install pandas numpy scikit-learn sqlalchemy websockets streamlit plotly seaborn matplotlib
```

---

# Running the System

The system requires **3 terminals running simultaneously**.

---

## Terminal 1 — Start Binance Data Stream

```
python -m data_ingestion.binance_stream
```

This streams real-time trades and stores them in:

```
crypto.db
```

---

## Terminal 2 — Run Pump Detector

```
python -m backend.auto_detector
```

Example output:

```
BTCUSDT pump probability: 0.02
SOLUSDT pump probability: 0.37
```

---

## Terminal 3 — Launch Dashboard

```
python -m streamlit run dashboard/app.py
```

Open dashboard in browser:

```
http://localhost:8501
```

---

# Example Dashboard

(Add screenshots here)

Example sections:

* Pump probability gauges
* Crypto market board
* Live price charts
* Volume activity heatmap
* Recent trades

---

# Technologies Used

### Programming

* Python

### Data Streaming

* Binance WebSocket API
* WebSockets

### Machine Learning

* Scikit-learn
* Random Forest Classifier

### Data Processing

* Pandas
* NumPy

### Database

* SQLite
* SQLAlchemy

### Visualization

* Streamlit
* Plotly
* Seaborn
* Matplotlib

---

# Future Improvements

Possible enhancements:

### Real-Time Alerts

Send notifications when pump probability exceeds threshold.

Example:

```
Pump detected for SOLUSDT
Probability: 0.92
```

### Sentiment Analysis

Analyze Twitter or Reddit sentiment to detect coordinated campaigns.

### Multi-Exchange Monitoring

Add support for:

* Coinbase
* Kraken
* KuCoin

### Deep Learning Models

Replace Random Forest with:

* LSTM
* Transformer-based time series models

```
