import requests
import time
from collections import deque
from telegram import Bot
import logging
import os

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Telegram Bot Token and Chat ID
TELEGRAM_BOT_TOKEN = '6607520248:AAGlWyz7086ivlLlRjgfhynykJawjz1HLl8'
CHAT_ID = '5016416878'
bot = Bot(TELEGRAM_BOT_TOKEN)

# Binance API URL for fetching Bitcoin price
BINANCE_API_URL = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'

# Thresholds for price change
PRICE_CHANGE_THRESHOLD_1_MIN = 1  # Percentage
PRICE_CHANGE_THRESHOLD_5_MIN = 2  # Percentage

# Store the last 300 prices (5 minutes of data at 1 price per second)
price_history = deque(maxlen=300)

# Time counters
one_minute_counter = 0
five_minute_counter = 0
one_hour_counter = 0

def get_bitcoin_price():
    try:
        response = requests.get(BINANCE_API_URL)
        response.raise_for_status()
        data = response.json()
        print(float(data['price']))
        return float(data['price'])
    except requests.RequestException as e:
        logging.error(f"Error fetching Bitcoin price from Binance: {e}")
        return None

def clear_screen():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For Mac and Linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def main():
    global one_minute_counter, five_minute_counter, one_hour_counter

    while True:
        current_price = get_bitcoin_price()
        if current_price is not None:
            price_history.append(current_price)
            one_minute_counter += 1
            five_minute_counter += 1
            one_hour_counter += 1

            if one_minute_counter >= 60:
                print(f"1 Minute BTC Price: {current_price}")
                one_minute_counter = 0

            if five_minute_counter >= 300:
                print(f"5 Minute BTC Price: {current_price}")
                five_minute_counter = 0

            if one_hour_counter >= 3600:
                clear_screen()
                one_hour_counter = 0

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()
