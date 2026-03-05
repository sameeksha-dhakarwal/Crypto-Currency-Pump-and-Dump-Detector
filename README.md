How to Run the Entire System

You now run three terminals:
venv
Terminal 1 — Market Data Stream
python -m data_ingestion.binance_stream
Terminal 2 — Pump Detection
python -m backend.auto_detector
Terminal 3 — Dashboard
streamlit run dashboard/app.py