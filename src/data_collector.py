import requests
from database_manager import insert_prices_to_db


def get_latest_prices():
    """
    Получает последние цены на Ethereum и Bitcoin с биржи Binance.

    Возвращает:
        Кортеж с последними ценами Ethereum и Bitcoin (float, float) или (None, None) в случае ошибки.
    """
    eth_url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    btc_url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    try:
        eth_response = requests.get(eth_url)
        btc_response = requests.get(btc_url)

        eth_price = float(eth_response.json()['price'])
        btc_price = float(btc_response.json()['price'])

        return eth_price, btc_price
    except Exception as e:
        print(f"Error fetching price data: {e}")
        return None, None


def collect_data():
    """
    Собирает данные о последних ценах на ETH и BTC и сохраняет их в базе данных.
    """
    eth_price, btc_price = get_latest_prices()
    if eth_price and btc_price:
        insert_prices_to_db(eth_price, btc_price)
