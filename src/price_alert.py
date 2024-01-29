import pandas as pd
from .database_manager import connect_to_db
from datetime import datetime, timedelta


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
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            SELECT eth_price, btc_price FROM price_data 
            WHERE timestamp >= %s
            ORDER BY timestamp ASC
            """
            one_hour_ago = datetime.now() - timedelta(hours=1)
            cursor.execute(query, (one_hour_ago,))
            records = cursor.fetchall()

            if records:
                # Преобразование Decimal в float
                start_eth_price = float(records[0][0])
                start_btc_price = float(records[0][1])
                end_eth_price = float(records[-1][0])
                end_btc_price = float(records[-1][1])

                eth_change = (end_eth_price - start_eth_price) / start_eth_price
                btc_change = (end_btc_price - start_btc_price) / start_btc_price

                # Создаем DataFrame для предсказания
                df_for_prediction = pd.DataFrame({'btc_return': [btc_change]})
                predicted_eth_change = regression_model.predict(df_for_prediction)[0]

                # Проверяем, отличается ли фактическое изменение ETH от предсказанного
                if abs(eth_change - predicted_eth_change) >= 0.01:
                    print(f"Значительное независимое изменение в цене ETH обнаружено: {end_eth_price}")
        except Exception as e:
            print(f"Ошибка при проверке изменения цен: {e}")
        finally:
            conn.close()
