import tkinter as tk
from tkinter import ttk, messagebox
from binance.client import Client
from binance.enums import *
import logging

# Logging setup
logging.basicConfig(filename='trading_bot_ui.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Replace with your Binance Futures Testnet API credentials
API_KEY = 'your_testnet_api_key'
API_SECRET = 'your_testnet_api_secret'

class BasicBot:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.futures_account()
            logging.info("Connected to Binance Futures Testnet.")
        except Exception as e:
            logging.error(f"Connection failed: {e}")
            raise e

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == 'MARKET':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity
                )
            elif order_type == 'LIMIT':
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_LIMIT,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price
                )
            else:
                raise ValueError("Unsupported order type.")

            logging.info(f"Order placed: {order}")
            return order
        except Exception as e:
            logging.error(f"Order failed: {e}")
            return {"error": str(e)}

# Create GUI
def run_ui():
    bot = BasicBot(API_KEY, API_SECRET)

    def submit_order():
        symbol = symbol_entry.get().upper()
        side = SIDE_BUY if side_var.get() == 'Buy' else SIDE_SELL
        order_type = order_type_var.get().upper()
        quantity = quantity_entry.get()
        price = price_entry.get()

        try:
            quantity = float(quantity)
            price = float(price) if order_type == 'LIMIT' else None
        except ValueError:
            messagebox.showerror("Input Error", "Invalid quantity or price.")
            return

        result = bot.place_order(symbol, side, order_type, quantity, price)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, str(result))

    # Root window
    root = tk.Tk()
    root.title("Binance Futures Trading Bot (Testnet)")

    # Layout
    tk.Label(root, text="Symbol:").grid(row=0, column=0, sticky='e')
    symbol_entry = tk.Entry(root)
    symbol_entry.grid(row=0, column=1)

    tk.Label(root, text="Side:").grid(row=1, column=0, sticky='e')
    side_var = tk.StringVar()
    side_menu = ttk.Combobox(root, textvariable=side_var, values=["Buy", "Sell"])
    side_menu.current(0)
    side_menu.grid(row=1, column=1)

    tk.Label(root, text="Order Type:").grid(row=2, column=0, sticky='e')
    order_type_var = tk.StringVar()
    order_type_menu = ttk.Combobox(root, textvariable=order_type_var, values=["MARKET", "LIMIT"])
    order_type_menu.current(0)
    order_type_menu.grid(row=2, column=1)

    tk.Label(root, text="Quantity:").grid(row=3, column=0, sticky='e')
    quantity_entry = tk.Entry(root)
    quantity_entry.grid(row=3, column=1)

    tk.Label(root, text="Price (for LIMIT):").grid(row=4, column=0, sticky='e')
    price_entry = tk.Entry(root)
    price_entry.grid(row=4, column=1)

    submit_btn = tk.Button(root, text="Place Order", command=submit_order)
    submit_btn.grid(row=5, column=0, columnspan=2, pady=10)

    tk.Label(root, text="Result:").grid(row=6, column=0, sticky='ne')
    result_text = tk.Text(root, height=10, width=50)
    result_text.grid(row=6, column=1)

    root.mainloop()

if __name__ == "__main__":
    run_ui()
