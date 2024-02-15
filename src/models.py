from sqlalchemy import Column, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PriceData(Base):
    """
    Определяет структуру таблицы цен для хранения данных о ценах на Ethereum и Bitcoin.

    Атрибуты:
        id: Уникальный идентификатор записи.
        timestamp: Временная метка добавления записи.
        eth_price: Цена Ethereum в момент времени.
        btc_price: Цена Bitcoin в момент времени.
    """
    __tablename__ = "price_data"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    eth_price = Column(Float)
    btc_price = Column(Float)
