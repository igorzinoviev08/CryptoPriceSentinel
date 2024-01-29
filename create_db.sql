-- Создание таблицы для хранения данных о ценах
CREATE TABLE price_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    eth_price NUMERIC NOT NULL,
    btc_price NUMERIC NOT NULL
);
