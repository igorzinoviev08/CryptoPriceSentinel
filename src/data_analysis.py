import pandas as pd
from sklearn.linear_model import LinearRegression

from database_manager import Session as session_factory
from models import PriceData


def _get_historical_data():
    """
    Получает исторические данные о ценах из базы данных с использованием ORM.

    Возвращает:
        Список объектов PriceData.
    """
    session = session_factory()
    try:
        return session.query(PriceData).order_by(PriceData.timestamp).all()
    finally:
        session.close()


def perform_regression_analysis():
    """
    Выполняет регрессионный анализ для определения взаимосвязи между изменениями цен на ETH и BTC.

    Использует исторические данные для вычисления процентных изменений цен и обучает на этих данных
    линейную регрессионную модель. Модель затем может быть использована для предсказания изменений
    цены ETH на основе изменений цены BTC.

    Выводит коэффициенты и перехват модели, объясняя их значение.

    Возвращает:
        Обученную модель линейной регрессии.
    """
    data = _get_historical_data()
    # Создание DataFrame из данных ORM
    df = pd.DataFrame(
        [(d.timestamp, d.eth_price, d.btc_price) for d in data],
        columns=["timestamp", "eth_price", "btc_price"],
    )

    df["eth_return"] = df["eth_price"].pct_change()
    df["btc_return"] = df["btc_price"].pct_change()
    df.dropna(inplace=True)

    X = df[["btc_return"]]
    y = df["eth_return"]
    model = LinearRegression().fit(X, y)

    # Вывод результатов
    print(
        f"""
    Результаты регрессионного анализа:
    Коэффициент (Coefficients): {model.coef_[0]:.4f}
    Это значение показывает, на сколько процентов изменяется цена ETH (eth_return),
    при изменении цены BTC (btc_return) на один процент.
    Положительный коэффициент указывает на прямую зависимость между ценами ETH и BTC.
    Отрицательный коэффициент указывает на обратную зависимость.

    Перехват (Intercept): {model.intercept_:.4f}
    Перехват (или точка пересечения с осью Y) показывает предсказанное значение изменения цены ETH (eth_return),
    когда изменение цены BTC (btc_return) равно нулю. В реальности это значение имеет ограниченную интерпретацию,
    поскольку цены на криптовалюту редко остаются статичными.
    """
    )
    return model
