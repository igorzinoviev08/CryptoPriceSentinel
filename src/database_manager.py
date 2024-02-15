from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from config import DB_URL
from models import PriceData

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)


def init_db():
    """
    Создает таблицы в базе данных на основе моделей.
    """
    Base.metadata.create_all(engine)


def insert_prices_to_db(eth_price, btc_price):
    """
    Добавляет цены ETH и BTC в базу данных.
    """
    session = Session()
    price_data = PriceData(
        timestamp=datetime.now(), eth_price=eth_price, btc_price=btc_price
    )
    session.add(price_data)
    session.commit()
    session.close()
