import asyncio
import json
import websockets
from database.db import store_trade

SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "bnbusdt",
    "solusdt",
    "dogeusdt"
]


async def stream_symbol(symbol):

    url = f"wss://stream.binance.com:9443/ws/{symbol}@trade"

    while True:
        try:

            async with websockets.connect(url) as websocket:

                print(f"Connected to {symbol}")

                while True:

                    data = await websocket.recv()
                    trade = json.loads(data)

                    price = float(trade["p"])
                    quantity = float(trade["q"])
                    timestamp = trade["T"]

                    print(symbol, price, quantity)

                    store_trade(symbol, price, quantity, timestamp)

        except Exception as e:

            print(f"Connection lost for {symbol}. Reconnecting...")
            await asyncio.sleep(5)


async def main():

    tasks = []

    for symbol in SYMBOLS:
        tasks.append(stream_symbol(symbol))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())