from datetime import datetime, timedelta

import pandas as pd

from database_manager import Session as session_factory
from models import PriceData


def _get_price_data_last_hour():
    """
    Получает записи о ценах ETH и BTC за последний час.
    """
    session = session_factory()
    one_hour_ago = datetime.now() - timedelta(hours=1)
    try:
        data = (
            session.query(PriceData)
            .filter(PriceData.timestamp >= one_hour_ago)
            .order_by(PriceData.timestamp.asc())
            .all()
        )
        return data
    finally:
        session.close()


def check_price_movement(regression_model):
    """
    Проверяет значительные независимые изменения в цене Ethereum (ETH) за последний час.

    Используя предоставленную регрессионную модель, функция сравнивает фактическое изменение
    цены ETH с предсказанным изменением на основе изменения цены Bitcoin (BTC).
    Предсказание основано на исторических данных о корреляции между ценами ETH и BTC.

    Args:
        regression_model: Обученная модель линейной регрессии для предсказания цены ETH.

    Выводит сообщение, если обнаруживается изменение цены ETH более чем на 1%,
    которое не соответствует ожидаемому изменению на основе цены BTC.
    """
    data = _get_price_data_last_hour()
    if data:
        # Преобразование данных в DataFrame
        df = pd.DataFrame(
            [(d.timestamp, d.eth_price, d.btc_price) for d in data],
            columns=["timestamp", "eth_price", "btc_price"],
        )

        start_eth_price = df.iloc[0]["eth_price"]
        start_btc_price = df.iloc[0]["btc_price"]
        end_eth_price = df.iloc[-1]["eth_price"]
        end_btc_price = df.iloc[-1]["btc_price"]

        eth_change = (end_eth_price - start_eth_price) / start_eth_price
        btc_change = (end_btc_price - start_btc_price) / start_btc_price

        # Создаем DataFrame для предсказания
        df_for_prediction = pd.DataFrame({"btc_return": [btc_change]})
        predicted_eth_change = regression_model.predict(df_for_prediction)[0]

        if abs(eth_change - predicted_eth_change) >= 0.01:
            print(
                f"Значительное независимое изменение в цене ETH обнаружено: {end_eth_price}"
            )
