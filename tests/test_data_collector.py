from src.data_collector import get_latest_prices


def test_get_latest_prices():
    eth_price, btc_price = get_latest_prices()
    assert eth_price is not None
    assert btc_price is not None
    assert isinstance(eth_price, float)
    assert isinstance(btc_price, float)
