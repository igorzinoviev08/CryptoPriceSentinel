from src.database_manager import connect_to_db, insert_prices_to_db


def test_connect_to_db():
    conn = connect_to_db()
    assert conn is not None


def test_insert_prices_to_db():
    # Предполагаем, что у вас есть тестовая база данных и соответствующие настройки
    conn = connect_to_db()
    assert conn is not None
    insert_prices_to_db(100.0, 200.0)  # Примерные тестовые данные
    # Здесь должна быть проверка успешного добавления данных в базу
