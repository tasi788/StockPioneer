import yfinance as yf


def test_yahoo():
    msft = yf.Ticker("AAPL")
    assert isinstance(msft.info, dict)
