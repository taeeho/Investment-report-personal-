import yfinance as yf


def fetch_financials(ticker_or_name):
    symbol = ticker_or_name.strip()
    if not symbol:
        return {}
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}
        keys = [
            "shortName",
            "marketCap",
            "trailingPE",
            "forwardPE",
            "priceToBook",
            "profitMargins",
            "revenueGrowth",
            "earningsGrowth",
            "dividendYield",
        ]
        return {key: info.get(key) for key in keys if key in info}
    except Exception:
        return {}
