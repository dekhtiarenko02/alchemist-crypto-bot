import tkinter as tk
from ccxt import async_support as ccxt
import asyncio


async def get_crypto_price(symbol):
    exchange = ccxt.binance()
    ticker = await exchange.fetch_ticker(symbol)
    return ticker['last']


class CryptoPriceViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Price Viewer")

        self.symbol_label = tk.Label(root, text="Symbol:")
        self.symbol_label.pack()

        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.pack()

        self.price_label = tk.Label(root, text="Price:")
        self.price_label.pack()

        self.price_value = tk.StringVar()
        self.price_entry = tk.Entry(root, textvariable=self.price_value, state="readonly")
        self.price_entry.pack()

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_price)
        self.refresh_button.pack()

    async def refresh_price(self):
        symbol = self.symbol_entry.get().upper()
        if symbol:
            loop = asyncio.get_event_loop()
            price = loop.run_until_complete(get_crypto_price(symbol))
            self.price_value.set(price)
        else:
            self.price_value.set("Enter a symbol")
