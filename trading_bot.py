import logging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import sys

logging.basicConfig(
    filename='trading_bot.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        try:
            self.client.futures_account()  
            logging.info("Connected to Binance Futures Testnet successfully.")
        except Exception as e:
            logging.error(f"Connection Error: {e}")
            sys.exit("Connection to Binance failed. Check your API keys and network.")

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

        except BinanceAPIException as e:
            logging.error(f"API Error: {e}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"General Error: {e}")
            return {"error": str(e)}

def get_user_input():
    try:
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        side_input = input("Buy or Sell? ").upper()
        side = SIDE_BUY if side_input == 'BUY' else SIDE_SELL
        order_type = input("Order type (MARKET/LIMIT): ").upper()
        quantity = float(input("Enter quantity: "))
        price = None
        if order_type == 'LIMIT':
            price = float(input("Enter limit price: "))
        return symbol, side, order_type, quantity, price
    except Exception as e:
        logging.error(f"Input Error: {e}")
        sys.exit("Invalid input. Exiting.")

if __name__ == "__main__":
    API_KEY = env.API_KEY = 'my_testnet_api_key'
    API_SECRET = env.API_SECRET = 'my_testnet_api_secret'

    bot = BasicBot(API_KEY, API_SECRET)

    symbol, side, order_type, quantity, price = get_user_input()
    response = bot.place_order(symbol, side, order_type, quantity, price)
    
    print("Order Response:")
    print(response)
