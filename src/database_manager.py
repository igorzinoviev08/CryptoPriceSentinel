import psycopg2
from datetime import datetime

from .config import DB_HOST, DB_NAME, DB_USER, DB_PASS

# Database configuration
db_config = {
    'host': DB_HOST,
    'database': DB_NAME,
    'user': DB_USER,
    'password': DB_PASS
}


def connect_to_db():
    """
    Устанавливает соединение с базой данных PostgreSQL.

    Возвращает:
        Объект соединения, если подключение успешно, иначе None.
    """
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None


def insert_prices_to_db(eth_price, btc_price):
    """
    Вставляет последние цены ETH и BTC в базу данных.

    Аргументы:
        eth_price (float): Последняя цена Ethereum.
        btc_price (float): Последняя цена Bitcoin.

    Примечания:
        Временная метка автоматически устанавливается на текущее время.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "INSERT INTO price_data (timestamp, eth_price, btc_price) VALUES (%s, %s, %s)"
            timestamp = datetime.now()
            cursor.execute(query, (timestamp, eth_price, btc_price))
            conn.commit()
        except Exception as e:
            print(f"Error inserting data into PostgreSQL database: {e}")
        finally:
            conn.close()


def get_historical_data():
    """
    Получает исторические данные о ценах из базы данных.

    Возвращает:
        Список кортежей, содержащих временные метки, цены ETH и BTC.
    """
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT timestamp, eth_price, btc_price FROM price_data ORDER BY timestamp"
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching historical data: {e}")
        finally:
            conn.close()
    return []
